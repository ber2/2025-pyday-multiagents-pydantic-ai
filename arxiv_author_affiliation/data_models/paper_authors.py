from pydantic import BaseModel

from arxiv_author_affiliation.data_models.author import Author


class PaperAuthors(BaseModel):
    arxiv_id: str
    authors: list[Author]

    @property
    def author_count(self) -> int:
        return len(self.authors)
