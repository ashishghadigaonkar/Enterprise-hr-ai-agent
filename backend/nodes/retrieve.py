import logging
from state import GraphState
from rag.retriever import retrieve_relevant_docs

logger = logging.getLogger("RetrieveNode")

def execute_rag_retrieval(state: GraphState) -> GraphState:
    """
    Executes document retrieval for HR_POLICY queries with logging and error handling.
    """
    try:
        if not state.get("auth_approved", False) or state.get("security_flag", False):
            logger.info(f"Skipping RAG retrieval for Query [{state.get('query_id')}] due to security/auth flag.")
            return state

        query = state.get("user_query", "")
        logger.info(f"Executing RAG retrieval node for Query [{state.get('query_id')}]: '{query}'")
        
        retrieved = retrieve_relevant_docs(query)

        return {
            **state,
            "tool_called": "RAGRetriever",
            "retrieved_docs": retrieved,
            "tool_output": f"Retrieved {len(retrieved)} policy document chunks."
        }
    except Exception as e:
        logger.error(f"Error in execute_rag_retrieval node: {e}", exc_info=True)
        return {
            **state,
            "tool_called": "RAGRetriever",
            "retrieved_docs": [],
            "tool_output": "RAG retrieval failed due to system error.",
            "error_message": str(e)
        }
