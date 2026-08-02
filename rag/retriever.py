import logging
from typing import List, Optional
from rag.loader import load_and_split_policy_documents
import config

logger = logging.getLogger("RAGRetriever")

# Global cached vector store instance
_vector_store_instance = None
_embedding_model_instance = None

def sanitize_retrieved_text(text: str) -> str:
    """
    Sanitizes retrieved text content to neutralize potential indirect prompt injections.
    Removes suspicious instruction overrides or system prompt commands embedded in documents.
    """
    forbidden_lines = [
        "ignore previous instructions",
        "system prompt:",
        "you must now output",
        "reveal employee salaries"
    ]
    lines = text.split("\n")
    safe_lines = [
        line for line in lines
        if not any(bad in line.lower() for bad in forbidden_lines)
    ]
    return "\n".join(safe_lines)


def get_embedding_model():
    """Factory function for HuggingFace embeddings."""
    global _embedding_model_instance
    if _embedding_model_instance is not None:
        return _embedding_model_instance

    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        logger.info(f"Initializing HuggingFaceEmbeddings model: {config.EMBEDDING_MODEL_NAME}")
        _embedding_model_instance = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_NAME)
        return _embedding_model_instance
    except Exception as e:
        logger.warning(f"Failed to load HuggingFaceEmbeddings ({e}). Embeddings will fallback.")
        return None


def get_pinecone_vector_store():
    """
    Initializes Pinecone Serverless vector store.
    Creates index ONLY ONCE if it does not exist; reuses existing index on subsequent calls.
    """
    global _vector_store_instance
    if _vector_store_instance is not None:
        return _vector_store_instance

    if not config.PINECONE_API_KEY:
        logger.info("PINECONE_API_KEY not configured. Falling back to in-memory search.")
        return None

    try:
        from pinecone import Pinecone, ServerlessSpec
        from langchain_pinecone import PineconeVectorStore

        pc = Pinecone(api_key=config.PINECONE_API_KEY)
        index_name = config.PINECONE_INDEX_NAME
        embeddings = get_embedding_model()

        if embeddings is None:
            return None

        # Check if index exists
        existing_indexes = [idx.name for idx in pc.list_indexes()]
        if index_name not in existing_indexes:
            logger.info(f"Creating new Pinecone Serverless index: '{index_name}'")
            pc.create_index(
                name=index_name,
                dimension=384,  # Dimension for all-MiniLM-L6-v2
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
            
            # Load chunks and populate new index
            docs = load_and_split_policy_documents()
            if docs:
                _vector_store_instance = PineconeVectorStore.from_documents(
                    documents=docs,
                    embedding=embeddings,
                    index_name=index_name
                )
                logger.info(f"Successfully created index '{index_name}' and indexed {len(docs)} document chunks.")
                return _vector_store_instance
        else:
            logger.info(f"Reusing existing Pinecone index: '{index_name}'")

        _vector_store_instance = PineconeVectorStore.from_existing_index(
            index_name=index_name,
            embedding=embeddings
        )
        return _vector_store_instance

    except Exception as e:
        logger.error(f"Pinecone vector store initialization failed: {e}. Falling back to keyword RAG.", exc_info=True)
        return None


def fallback_keyword_retrieval(query: str, top_k: int) -> List[str]:
    """Fallback retriever when Pinecone vector database is unconfigured or unreachable."""
    docs = load_and_split_policy_documents()
    if not docs:
        return []

    query_tokens = set(query.lower().split())
    scored_docs = []
    for doc in docs:
        content_lower = doc.page_content.lower()
        score = sum(1 for token in query_tokens if token in content_lower)
        scored_docs.append((score, doc))

    scored_docs.sort(key=lambda x: x[0], reverse=True)

    results = []
    for score, doc in scored_docs[:top_k]:
        cleaned_content = sanitize_retrieved_text(doc.page_content)
        doc_summary = f"[{doc.metadata.get('source', 'policy.txt')}]\n{cleaned_content}"
        results.append(doc_summary)

    return results


def retrieve_relevant_docs(query: str, top_k: int = config.TOP_K_RETRIEVAL) -> List[str]:
    """
    Retrieves top_k policy documents relevant to query.
    Uses Pinecone vector similarity search if available, otherwise falls back gracefully.
    Applies security sanitization to retrieved contents.
    """
    try:
        vector_store = get_pinecone_vector_store()
        if vector_store is not None:
            logger.info(f"Performing Pinecone vector similarity search for query: '{query}'")
            results_docs = vector_store.similarity_search(query, k=top_k)
            retrieved = []
            for doc in results_docs:
                cleaned_content = sanitize_retrieved_text(doc.page_content)
                source_name = doc.metadata.get("source", "policy.txt")
                retrieved.append(f"[{source_name}]\n{cleaned_content}")
            return retrieved
    except Exception as e:
        logger.warning(f"Pinecone similarity search error ({e}). Using keyword fallback.")

    logger.info(f"Using fallback retrieval for query: '{query}'")
    return fallback_keyword_retrieval(query, top_k)
