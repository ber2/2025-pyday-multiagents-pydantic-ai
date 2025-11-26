from pydantic import BaseModel, Field

from arxiv_author_affiliation.data_models.affiliation import Affiliation


class Author(BaseModel):
    name: str
    affiliations: list[Affiliation] = Field(default_factory=list)
