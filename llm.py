import config
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from pydantic import Field

class MockLLM(BaseChatModel):
    """Fallback LLM for offline testing or when API keys are not provided."""

    def _generate(self, messages: list[BaseMessage], stop=None, run_manager=None, **kwargs) -> ChatResult:
        full_msg = messages[-1].content if messages else ""
        
        # Extract user query if embedded in prompt template
        if 'Query: "' in full_msg:
            query_part = full_msg.split('Query: "')[-1].split('"')[0].lower()
        else:
            query_part = full_msg.lower()

        # Deterministic response generation for test scenarios
        if "draft a clear" in full_msg.lower() or "context information" in full_msg.lower():
            if "Tool Data:" in full_msg:
                tool_data = full_msg.split("Tool Data:")[-1].split("\n")[0].strip()
                content = f"Here is your requested information: {tool_data}"
            elif "Retrieved Policies:" in full_msg:
                content = "According to company policy, unused PTO days up to 5 days can be rolled over to the next year."
            else:
                content = "Here is the general information requested."
        elif "pto" in query_part or "vacation" in query_part:
            if "rollover" in query_part or "policy" in query_part:
                content = "HR_POLICY"
            else:
                content = "PTO"
        elif "expense" in query_part or "receipt" in query_part or "reimbursement" in query_part:
            content = "EXPENSE"
        elif "it" in query_part or "access" in query_part or "password" in query_part or "vpn" in query_part:
            content = "IT_ACCESS"
        elif "policy" in query_part or "rule" in query_part:
            content = "HR_POLICY"
        else:
            content = "GENERAL"

        generation = ChatGeneration(message=AIMessage(content=content))
        return ChatResult(generations=[generation])

    @property
    def _llm_type(self) -> str:
        return "mock-llm"


def get_llm(temperature: float = 0.0) -> BaseChatModel:
    """
    Factory function to return configured LLM provider.
    Defaults to Groq if key is present, otherwise falls back to MockLLM.
    """
    provider = config.LLM_PROVIDER.lower()

    if provider == "groq" and config.GROQ_API_KEY:
        try:
            from langchain_groq import ChatGroq
            return ChatGroq(
                groq_api_key=config.GROQ_API_KEY,
                model_name=config.GROQ_MODEL_NAME,
                temperature=temperature
            )
        except Exception as e:
            print(f"[Warning] Failed to initialize ChatGroq ({e}). Falling back to MockLLM.")

    elif provider == "openai" and config.OPENAI_API_KEY:
        try:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                api_key=config.OPENAI_API_KEY,
                model_name=config.OPENAI_MODEL_NAME,
                temperature=temperature
            )
        except Exception as e:
            print(f"[Warning] Failed to initialize ChatOpenAI ({e}). Falling back to MockLLM.")

    # Default fallback when API keys are not provided
    return MockLLM()
