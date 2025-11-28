from pydantic import BaseModel, Field

from arxiv_author_affiliation.data_models.author import Author
from arxiv_author_affiliation.data_models.normalized_affiliation import (
    NormalizedAffiliation,
)


class ValidatedPaper(BaseModel):
    arxiv_id: str
    authors: list[Author]
    normalized_affiliations: list[NormalizedAffiliation]
    validation_issues: list[str] = Field(default_factory=list)
