import csv
import logging
from datetime import datetime
import config
from state import GraphState

logger = logging.getLogger("AuditNode")

def audit_logger(state: GraphState) -> GraphState:
    """
    Logs query execution metrics, security decisions, tools used, trace_id, and response to CSV.
    Updates audit_record in GraphState and appends row to outputs/results.csv.
    Includes exception handling and logging.
    """
    try:
        timestamp = datetime.now().isoformat()

        trace_id = state.get("trace_id", "N/A")
        query_id = state.get("query_id", "Q-UNKNOWN")
        employee_id = state.get("employee_id", "N/A")
        intent = state.get("intent", "GENERAL")
        security_flag = state.get("security_flag", False)
        auth_approved = state.get("auth_approved", True)
        tool_called = state.get("tool_called", "None")
        retrieved_docs = state.get("retrieved_docs", [])
        retrieved_str = "; ".join(retrieved_docs) if retrieved_docs else "None"
        final_response = state.get("final_response", "")
        confidence = state.get("confidence", "Low")

        audit_record = {
            "timestamp": timestamp,
            "trace_id": trace_id,
            "query_id": query_id,
            "employee_id": employee_id,
            "intent": intent,
            "accessed_documents": retrieved_str,
            "tools_called": tool_called,
            "authorization_decision": "Approved" if auth_approved else "Denied",
            "security_decision": "Flagged" if security_flag else "Safe",
            "answer": final_response,
            "confidence": confidence,
            "security_flag": security_flag
        }

        # Append to outputs/results.csv
        file_exists = config.RESULTS_CSV.exists()

        fieldnames = [
            "query_id", "employee_id", "intent", "answer",
            "confidence", "security_flag", "tool_used", "retrieved_docs",
            "authorization_decision", "security_decision", "trace_id", "timestamp"
        ]

        with open(config.RESULTS_CSV, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()

            writer.writerow({
                "query_id": query_id,
                "employee_id": employee_id,
                "intent": intent,
                "answer": final_response,
                "confidence": confidence,
                "security_flag": security_flag,
                "tool_used": tool_called,
                "retrieved_docs": retrieved_str,
                "authorization_decision": "Approved" if auth_approved else "Denied",
                "security_decision": "Flagged" if security_flag else "Safe",
                "trace_id": trace_id,
                "timestamp": timestamp
            })

        logger.info(f"Audit log entry saved for Query [{query_id}] (Trace: {trace_id}) to {config.RESULTS_CSV}")
        return {
            **state,
            "audit_record": audit_record
        }
    except Exception as e:
        logger.error(f"Error in audit_logger node: {e}", exc_info=True)
        return {
            **state,
            "error_message": str(e)
        }
