import logging
import pandas as pd
import config
from state import GraphState

logger = logging.getLogger("ToolsNode")

def load_employee_db():
    """Reads employees.csv safely."""
    try:
        if not config.EMPLOYEES_CSV.exists():
            return None
        return pd.read_csv(config.EMPLOYEES_CSV)
    except Exception as e:
        logger.error(f"Failed to load employees CSV in tools: {e}")
        return None

def execute_pto_tool(state: GraphState) -> GraphState:
    """Handles PTO queries and balance retrieval."""
    try:
        if not state.get("auth_approved", False):
            return state

        emp_id = state.get("employee_id", "").upper()
        df = load_employee_db()

        if df is None:
            output = "PTO Tool Error: Employee database unavailable."
        else:
            matches = df[df["employee_id"] == emp_id]
            if matches.empty:
                output = f"PTO Tool Error: Employee record '{emp_id}' not found."
            else:
                emp_data = matches.iloc[0]
                output = f"PTO Balance for {emp_data['name']} ({emp_id}): {emp_data['pto_balance']} days available."

        logger.info(f"PTO tool executed for Query [{state.get('query_id')}]: {output}")
        return {
            **state,
            "tool_called": "LeaveTool",
            "tool_output": output
        }
    except Exception as e:
        logger.error(f"Error in execute_pto_tool: {e}", exc_info=True)
        return {
            **state,
            "tool_called": "LeaveTool",
            "tool_output": "PTO tool execution failed due to an internal error.",
            "error_message": str(e)
        }


def execute_expense_tool(state: GraphState) -> GraphState:
    """Handles expense balance and reimbursement inquiries."""
    try:
        if not state.get("auth_approved", False):
            return state

        emp_id = state.get("employee_id", "").upper()
        df = load_employee_db()

        if df is None:
            output = "Expense Tool Error: Employee database unavailable."
        else:
            matches = df[df["employee_id"] == emp_id]
            if matches.empty:
                output = f"Expense Tool Error: Employee record '{emp_id}' not found."
            else:
                emp_data = matches.iloc[0]
                output = f"Expense limit for {emp_data['name']} ({emp_id}): ${emp_data['expense_limit']:.2f} per claim."

        logger.info(f"Expense tool executed for Query [{state.get('query_id')}]: {output}")
        return {
            **state,
            "tool_called": "ExpenseTool",
            "tool_output": output
        }
    except Exception as e:
        logger.error(f"Error in execute_expense_tool: {e}", exc_info=True)
        return {
            **state,
            "tool_called": "ExpenseTool",
            "tool_output": "Expense tool execution failed due to an internal error.",
            "error_message": str(e)
        }


def execute_it_tool(state: GraphState) -> GraphState:
    """Handles IT access and security system requests."""
    try:
        if not state.get("auth_approved", False):
            return state

        emp_id = state.get("employee_id", "").upper()
        df = load_employee_db()

        if df is None:
            dept = "General"
            name = emp_id
        else:
            matches = df[df["employee_id"] == emp_id]
            if matches.empty:
                dept = "General"
                name = emp_id
            else:
                emp_data = matches.iloc[0]
                dept = emp_data.get('department', 'General')
                name = emp_data.get('name', emp_id)

        output = f"IT Ticket created for {name} ({emp_id}). Department: {dept}. MFA/Access review initiated."
        logger.info(f"IT tool executed for Query [{state.get('query_id')}]: {output}")
        return {
            **state,
            "tool_called": "ITAccessTool",
            "tool_output": output
        }
    except Exception as e:
        logger.error(f"Error in execute_it_tool: {e}", exc_info=True)
        return {
            **state,
            "tool_called": "ITAccessTool",
            "tool_output": "IT tool execution failed due to an internal error.",
            "error_message": str(e)
        }
