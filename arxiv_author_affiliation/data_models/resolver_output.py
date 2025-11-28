from pydantic import BaseModel, Field

from arxiv_author_affiliation.data_models.normalized_affiliation import (
    NormalizedAffiliation,
)


class ResolverOutput(BaseModel):
    normalized_affiliations: list[NormalizedAffiliation]
    needs_clarification: bool = False
    issues: list[str] = Field(default_factory=list)
