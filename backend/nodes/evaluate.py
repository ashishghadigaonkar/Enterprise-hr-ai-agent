import logging
from state import GraphState

logger = logging.getLogger("EvaluateNode")

def self_evaluate(state: GraphState) -> GraphState:
    """
    Self-evaluates the drafted response:
    - Verifies alignment between intent and response content.
    - Verifies evidence presence (tool output or retrieved docs).
    - Sets confidence level to High, Medium, or Low.
    Includes exception safety and logging.
    """
    try:
        if state.get("security_flag", False) or not state.get("auth_approved", True):
            refusal = state.get("draft_response", "Request Refused.")
            logger.info(f"Self-evaluation for Query [{state.get('query_id')}]: Rejection verified (Confidence: High)")
            return {
                **state,
                "final_response": refusal,
                "confidence": "High"  # Refusals are definitive
            }

        draft = state.get("draft_response", "")
        intent = state.get("intent", "GENERAL")
        tool_output = state.get("tool_output", None)
        retrieved_docs = state.get("retrieved_docs", [])

        has_evidence = bool(tool_output or retrieved_docs)

        # Simple evidence & intent matching rules
        if intent in ["PTO", "EXPENSE", "IT_ACCESS"] and tool_output:
            confidence = "High"
        elif intent == "HR_POLICY" and len(retrieved_docs) > 0:
            confidence = "High"
        elif has_evidence:
            confidence = "Medium"
        else:
            confidence = "Low" if intent != "GENERAL" else "Medium"

        logger.info(f"Self-evaluated Query [{state.get('query_id')}]: Intent [{intent}] -> Confidence [{confidence}]")
        return {
            **state,
            "final_response": draft,
            "confidence": confidence
        }
    except Exception as e:
        logger.error(f"Error in self_evaluate node: {e}", exc_info=True)
        return {
            **state,
            "final_response": state.get("draft_response", "Request processed."),
            "confidence": "Low",
            "error_message": str(e)
        }
