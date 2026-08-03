import logging
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import config

logger = logging.getLogger("RAGLoader")

def load_and_split_policy_documents(chunk_size: int = 500, chunk_overlap: int = 50) -> List[Document]:
    """
    Reads plaintext policy documents from POLICY_DOCS_DIR and splits them into
    chunks using RecursiveCharacterTextSplitter.
    Returns a list of LangChain Document objects.
    """
    docs: List[Document] = []
    policy_dir = config.POLICY_DOCS_DIR

    if not policy_dir.exists():
        logger.warning(f"Policy directory does not exist: {policy_dir}")
        return docs

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    for file_path in policy_dir.glob("*.txt"):
        try:
            content = file_path.read_text(encoding="utf-8")
            raw_doc = Document(
                page_content=content,
                metadata={"source": file_path.name, "doc_id": file_path.stem}
            )
            chunks = splitter.split_documents([raw_doc])
            docs.extend(chunks)
            logger.info(f"Loaded '{file_path.name}': split into {len(chunks)} chunks.")
        except Exception as e:
            logger.error(f"Failed to read policy file '{file_path}': {e}")

    return docs
