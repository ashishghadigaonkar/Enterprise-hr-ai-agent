import logging
from state import GraphState
from llm import get_llm

logger = logging.getLogger("ClassifyNode")
VALID_INTENTS = ["PTO", "IT_ACCESS", "EXPENSE", "HR_POLICY", "GENERAL"]

def classify_intent(state: GraphState) -> GraphState:
    """
    Classifies user query into one of: PTO, IT_ACCESS, EXPENSE, HR_POLICY, GENERAL.
    Includes exception handling and logging.
    """
    try:
        if state.get("security_flag", False):
            logger.info(f"Skipping classification for Query [{state.get('query_id')}] due to security flag.")
            return state

        query = state.get("user_query", "").strip()
        logger.info(f"Classifying intent for Query [{state.get('query_id')}]: '{query}'")

        llm = get_llm(temperature=0.0)
        prompt = (
            f"Classify the following query into exactly one category: {', '.join(VALID_INTENTS)}.\n"
            f"Query: \"{query}\"\n"
            "Return only the category name."
        )

        response = llm.invoke(prompt)
        content = response.content.strip().upper()

        intent = "GENERAL"
        for valid in VALID_INTENTS:
            if valid in content:
                intent = valid
                break

        logger.info(f"Classified Query [{state.get('query_id')}] intent as: {intent}")
        return {
            **state,
            "intent": intent
        }
    except Exception as e:
        logger.error(f"Error in classify_intent node: {e}. Defaulting to GENERAL.", exc_info=True)
        return {
            **state,
            "intent": "GENERAL",
            "error_message": str(e)
        }
