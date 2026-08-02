from typing import TypedDict, List, Optional, Dict, Any

class GraphState(TypedDict, total=False):
    """
    LangGraph state schema passed between nodes in the workflow.
    """
    trace_id: str
    query_id: str
    user_query: str
    employee_id: str
    intent: str  # PTO, IT_ACCESS, EXPENSE, HR_POLICY, GENERAL
    security_flag: bool
    security_reason: str
    auth_approved: bool
    auth_reason: str
    retrieved_docs: List[str]
    tool_called: Optional[str]
    tool_output: Optional[str]
    draft_response: str
    final_response: str
    confidence: str  # High, Medium, Low
    audit_record: Dict[str, Any]
    error_message: Optional[str]
