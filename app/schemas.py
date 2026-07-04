from pydantic import BaseModel, Field
from enum import Enum

class PromptConfig(BaseModel):
    version: str
    created_at: str
    description: str
    system_prompt: str

    
class EmailCategory(str, Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    ACCOUNT = "account"
    GENERAL = "general"


class EmailResult(BaseModel):
    category: EmailCategory = Field(
        description="Category of the customer email."
    )
    summary: str = Field(
        description="One-sentence summary of the email."
    )


class EvaluationResult(BaseModel):
    id: str

    expected_category: EmailCategory

    predicted_category: EmailCategory

    expected_summary: str

    predicted_summary: str

    passed: bool

    latency_ms: float

class EvaluationReport(BaseModel):

    prompt_version: str

    total_cases: int

    passed_cases: int

    failed_cases: int

    accuracy: float

    results: list[EvaluationResult]