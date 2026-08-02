import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from nodes.tools import execute_pto_tool, execute_expense_tool, execute_it_tool

def test_pto_tool():
    state = {"query_id": "T1", "employee_id": "EMP101", "auth_approved": True}
    result = execute_pto_tool(state)
    assert result.get("tool_called") == "LeaveTool"
    assert "15 days" in result.get("tool_output", "")

def test_expense_tool():
    state = {"query_id": "T1", "employee_id": "EMP102", "auth_approved": True}
    result = execute_expense_tool(state)
    assert result.get("tool_called") == "ExpenseTool"
    assert "1200.00" in result.get("tool_output", "")

def test_it_tool():
    state = {"query_id": "T1", "employee_id": "EMP103", "auth_approved": True}
    result = execute_it_tool(state)
    assert result.get("tool_called") == "ITAccessTool"
    assert "Human Resources" in result.get("tool_output", "")
