import re
import logging
import pandas as pd
import config
from state import GraphState

logger = logging.getLogger("AuthorizationNode")

def load_employee_db():
    """Reads employees.csv mock database safely."""
    try:
        if not config.EMPLOYEES_CSV.exists():
            logger.error(f"Employee database CSV missing at path: {config.EMPLOYEES_CSV}")
            return None
        return pd.read_csv(config.EMPLOYEES_CSV)
    except Exception as e:
        logger.error(f"Error loading employee DB: {e}")
        return None

def check_authorization(state: GraphState) -> GraphState:
    """
    Authorization check node.
    Rules:
    - Employee must exist in employees.csv database.
    - Prevents cross-employee data access using exact regex word boundaries (e.g. EMP101 requesting EMP102).
    - Returns graceful refusal responses when authorization fails.
    """
    try:
        if state.get("security_flag", False):
            return state

        emp_id = state.get("employee_id", "").strip().upper()
        query = state.get("user_query", "")

        df = load_employee_db()
        if df is None:
            logger.error("Employee DB unavailable during authorization check.")
            refusal = "Authorization Refusal: System database is temporarily unavailable."
            return {
                **state,
                "auth_approved": False,
                "auth_reason": "Database unavailable.",
                "draft_response": refusal,
                "final_response": refusal,
                "confidence": "High"
            }

        # Check if requesting employee exists
        valid_ids = [str(x).strip().upper() for x in df["employee_id"].values]
        if emp_id not in valid_ids:
            logger.warning(f"Authorization failed: Employee ID '{emp_id}' not found in database.")
            refusal = f"Access Refusal: Employee ID '{emp_id}' is invalid or not registered in the employee directory."
            return {
                **state,
                "auth_approved": False,
                "auth_reason": f"Employee ID '{emp_id}' not found in database.",
                "draft_response": refusal,
                "final_response": refusal,
                "confidence": "High"
            }

        # Check for unauthorized cross-employee access attempts using regex word boundaries
        other_emp_ids = [id_ for id_ in valid_ids if id_ != emp_id]
        for other_id in other_emp_ids:
            pattern = re.compile(rf"\b{re.escape(other_id)}\b", re.IGNORECASE)
            if pattern.search(query):
                logger.warning(f"Cross-employee access blocked: [{emp_id}] attempted access to [{other_id}] in Query [{state.get('query_id')}]")
                refusal = f"Access Refusal: Employee '{emp_id}' is not authorized to query confidential records of '{other_id}'."
                return {
                    **state,
                    "auth_approved": False,
                    "auth_reason": f"Cross-employee access attempted for target '{other_id}'.",
                    "draft_response": refusal,
                    "final_response": refusal,
                    "confidence": "High"
                }

        logger.info(f"Authorization approved for Employee [{emp_id}] in Query [{state.get('query_id')}]")
        return {
            **state,
            "auth_approved": True,
            "auth_reason": "Authorized: Query matches permitted employee boundary."
        }
    except Exception as e:
        logger.error(f"Error in check_authorization node: {e}", exc_info=True)
        return {
            **state,
            "auth_approved": False,
            "auth_reason": f"Authorization node error: {str(e)}",
            "error_message": str(e),
            "draft_response": "Access Refusal: Unable to complete authorization check due to an internal system error."
        }
