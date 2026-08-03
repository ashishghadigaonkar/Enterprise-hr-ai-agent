import logging
from state import GraphState

logger = logging.getLogger("InputGuard")

def validate_input(state: GraphState) -> GraphState:
    """
    Validates user query input and employee ID.
    Ensures query is non-empty and employee_id is provided.
    Includes exception handling and logging.
    """
    try:
        query = state.get("user_query", "").strip() if state.get("user_query") else ""
        emp_id = state.get("employee_id", "").strip() if state.get("employee_id") else ""

        if not query:
            logger.warning(f"Input validation failed: Empty query for ID {state.get('query_id')}")
            return {
                **state,
                "security_flag": True,
                "security_reason": "Empty or whitespace user query.",
                "draft_response": "Request rejected: Query cannot be empty.",
                "final_response": "Request rejected: Query cannot be empty.",
                "confidence": "High"
            }

        if not emp_id:
            logger.warning(f"Input validation failed: Missing employee ID for Query {state.get('query_id')}")
            return {
                **state,
                "security_flag": True,
                "security_reason": "Missing employee ID.",
                "draft_response": "Request rejected: Employee ID is required for verification.",
                "final_response": "Request rejected: Employee ID is required for verification.",
                "confidence": "High"
            }

        logger.info(f"Input validation passed for Query [{state.get('query_id')}] - Emp [{emp_id}]")
        return {
            **state,
            "security_flag": False,
            "security_reason": ""
        }
    except Exception as e:
        logger.error(f"Error in validate_input node: {e}", exc_info=True)
        return {
            **state,
            "security_flag": True,
            "security_reason": f"Input validation error: {str(e)}",
            "error_message": str(e),
            "draft_response": "Request rejected due to internal input validation failure."
        }
