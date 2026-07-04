import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.llm import define_llm
from app.schemas import EmailResult
from app.prompts import load_prompt
import httpx
from app.schemas import EmailCategory

# Lazy-initialize the LLM to avoid blocking on import-time network/setup operations
llm = None
structured_llm = None


def _get_structured_llm():
    global llm, structured_llm
    if structured_llm is None:
        llm = define_llm()
        structured_llm = llm.with_structured_output(EmailResult)
    return structured_llm


def classify_email(email: str, prompt_version: str = "v1") -> EmailResult:
    """
    Classifies a customer support email and returns the category and summary.
    """

    prompt_config = load_prompt(prompt_version)

    prompt = f"""
{prompt_config.system_prompt}

Customer Email:
{email}
""" 
    # print(prompt_config.version)
    # print("\n\n\n -------")
    # print(prompt_config.system_prompt)
    # print("\n\n\n -------")

    structured = _get_structured_llm()
    try:
        return structured.invoke(prompt)
    except httpx.ConnectError as exc:
        # LLM service unreachable: return a safe fallback result so the app doesn't hang
        print("LLM connection failed:", exc)
        return EmailResult(
            category=EmailCategory.GENERAL,
            summary="LLM unavailable — placeholder summary"
        )



