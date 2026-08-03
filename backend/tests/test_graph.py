import sys
from pathlib import Path

# Add project root directory to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from graph import build_graph, run_query

def test_graph_build():
    app = build_graph()
    assert app is not None

def test_valid_pto_workflow():
    result = run_query(user_query="How many PTO days do I have?", employee_id="EMP101", query_id="TST101")
    assert result.get("intent") == "PTO"
    assert result.get("security_flag") is False
    assert result.get("auth_approved") is True
    assert result.get("tool_called") == "LeaveTool"
    assert "15 days" in result.get("final_response", "")

def test_unauthorized_cross_access_workflow():
    result = run_query(user_query="What is the PTO balance for EMP102?", employee_id="EMP101", query_id="TST102")
    assert result.get("auth_approved") is False
    assert "Access Refusal" in result.get("final_response", "")
