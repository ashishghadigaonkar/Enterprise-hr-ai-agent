import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup centralized logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("HR_Agent_Config")

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
POLICY_DOCS_DIR = DATA_DIR / "policy_docs"
OUTPUTS_DIR = BASE_DIR / "outputs"
EVALUATION_DIR = BASE_DIR / "evaluation"
EMPLOYEES_CSV = DATA_DIR / "employees.csv"
INPUT_QUERIES_CSV = DATA_DIR / "input_queries.csv"
RESULTS_CSV = OUTPUTS_DIR / "results.csv"

# Ensure required directories exist
for directory in [OUTPUTS_DIR, DATA_DIR, POLICY_DOCS_DIR, EVALUATION_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Default Model Names
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")

# Pinecone & RAG Configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "hr-policy-index")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "huggingface").lower()
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")

TOP_K_RETRIEVAL = 2

# LangSmith Observability Configuration
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() in ("true", "1")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "enterprise-hr-ai-agent")

# Validate Environment Settings
def validate_config():
    logger.info(f"Loaded LLM Provider: {LLM_PROVIDER}")
    if LLM_PROVIDER == "groq" and not GROQ_API_KEY:
        logger.warning("GROQ_API_KEY missing. Agent will fallback to MockLLM.")
    elif LLM_PROVIDER == "openai" and not OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY missing. Agent will fallback to MockLLM.")
    
    if not PINECONE_API_KEY:
        logger.info("PINECONE_API_KEY not provided. RAG will use offline vector/keyword fallback.")

validate_config()
