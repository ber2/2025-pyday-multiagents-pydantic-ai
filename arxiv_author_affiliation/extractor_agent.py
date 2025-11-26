from pydantic_ai import Agent

from arxiv_author_affiliation.data_models.paper_authors import PaperAuthors


def extract_authors(arxiv_id: str, paper_text: str) -> PaperAuthors:
    raise NotImplementedError("Extractor agent not yet implemented")
