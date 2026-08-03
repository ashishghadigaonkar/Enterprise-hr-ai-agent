import logging
from state import GraphState
from llm import get_llm

logger = logging.getLogger("DraftNode")

def draft_response(state: GraphState) -> GraphState:
    """
    Synthesizes tool output, retrieved docs, or general knowledge into a clean draft response.
    Preserves security or authorization rejections. Includes logging and exception safety.
    """
    try:
        # If blocked by security or authorization, keep existing rejection response
        if state.get("security_flag", False) or not state.get("auth_approved", True):
            existing_refusal = state.get("draft_response", "Request Refused due to security or authorization policy.")
            logger.info(f"Preserving rejection response for Query [{state.get('query_id')}]")
            return {
                **state,
                "draft_response": existing_refusal
            }

        query = state.get("user_query", "")
        intent = state.get("intent", "GENERAL")
        tool_output = state.get("tool_output", "")
        retrieved_docs = state.get("retrieved_docs", [])

        context_str = ""
        if tool_output:
            context_str += f"\nTool Data: {tool_output}"
        if retrieved_docs:
            context_str += "\nRetrieved Policies:\n" + "\n---\n".join(retrieved_docs)

        logger.info(f"Drafting response for Query [{state.get('query_id')}] with intent [{intent}]")

        prompt = (
            f"You are a helpful HR Assistant.\n"
            f"User Query: \"{query}\"\n"
            f"Intent: {intent}\n"
            f"Context Information:\n{context_str}\n\n"
            "Draft a clear, polite, and accurate response based ONLY on the provided context information. "
            "If no specific tool data or policies apply, answer standardly and professionally."
        )

        llm = get_llm(temperature=0.2)
        response = llm.invoke(prompt)
        draft = response.content.strip()

        return {
            **state,
            "draft_response": draft
        }
    except Exception as e:
        logger.error(f"Error in draft_response node: {e}. Fallback synthesis applied.", exc_info=True)
        tool_output = state.get("tool_output", "")
        retrieved_docs = state.get("retrieved_docs", [])
        fallback_draft = tool_output if tool_output else (retrieved_docs[0] if retrieved_docs else "Request processed successfully.")
        return {
            **state,
            "draft_response": fallback_draft,
            "error_message": str(e)
        }
