from pydantic import BaseModel

from arxiv_author_affiliation.data_models.author import Author


class ValidatedPaper(BaseModel):
    pass
