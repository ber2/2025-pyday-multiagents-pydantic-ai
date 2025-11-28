from pydantic import BaseModel


class NormalizedAffiliation(BaseModel):
    original_name: str
    normalized_name: str
    is_valid: bool
    confidence: float
