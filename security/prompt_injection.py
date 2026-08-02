import re
import logging
from state import GraphState

logger = logging.getLogger("PromptInjectionGuard")

# Regex patterns for direct and indirect prompt injection attempts
PROMPT_INJECTION_REGEXES = [
    r"(?i)\bignore\s+(all|previous|prior)\s+(instructions|rules|prompts)\b",
    r"(?i)\bdisregard\s+(prior|previous)\s+(rules|system|directives)\b",
    r"(?i)\breveal\s+(employee\s+)?(salaries|salary|credentials|passwords|system\s+prompt)\b",
    r"(?i)\bshow\s+(me\s+)?(system\s+prompt|developer\s+instructions|hidden\s+rules)\b",
    r"(?i)\bbypass\s+(security|authorization|rules|guardrails)\b",
    r"(?i)\bdump\s+(database|tables|employees|users)\b",
    r"(?i)\badmin\s+(override|mode|access|privileges)\b",
    r"(?i)\bact\s+as\s+an?\s+unrestricted\b",
    r"(?i)\bsystem\s*:\s*override\b"
]

COMPILED_PATTERNS = [re.compile(p) for p in PROMPT_INJECTION_REGEXES]

def check_prompt_injection(state: GraphState) -> GraphState:
    """
    Scans user query using regex patterns to detect prompt injection or security exploitation attempts.
    Sets security_flag=True and populates a graceful refusal response if detected.
    """
    try:
        # Pass through if already flagged by input_guard
        if state.get("security_flag", False):
            return state

        query = state.get("user_query", "")

        for pattern in COMPILED_PATTERNS:
            match = pattern.search(query)
            if match:
                matched_text = match.group(0)
                logger.warning(f"Prompt injection detected for Query [{state.get('query_id')}]: Matched '{matched_text}'")
                refusal_msg = "Security Policy Refusal: Your request contains patterns that violate our security policy and cannot be processed."
                return {
                    **state,
                    "security_flag": True,
                    "security_reason": f"Prompt injection detected via regex pattern: '{matched_text}'",
                    "draft_response": refusal_msg,
                    "final_response": refusal_msg,
                    "confidence": "High"
                }

        logger.info(f"Prompt injection check passed for Query [{state.get('query_id')}]")
        return {
            **state,
            "security_flag": False,
            "security_reason": ""
        }
    except Exception as e:
        logger.error(f"Error in check_prompt_injection node: {e}", exc_info=True)
        return {
            **state,
            "security_flag": True,
            "security_reason": f"Prompt injection node exception: {str(e)}",
            "error_message": str(e),
            "draft_response": "Security Policy Refusal: Unable to process request due to a security inspection anomaly."
        }
