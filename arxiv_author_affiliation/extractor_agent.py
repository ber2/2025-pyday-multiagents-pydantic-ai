import os
from pydantic_ai import Agent

from arxiv_author_affiliation.data_models.paper_authors import PaperAuthors


SYSTEM_PROMPT = """
You are an expert at extracting structured author and affiliation data from academic papers.

Extract all authors and their affiliations from the provided paper text.
For each author, include:
- Their full name
- All affiliations listed for that author

Return the data in the structured format.
"""


def extract_authors(arxiv_id: str, paper_text: str) -> PaperAuthors:
    model_name = os.environ["MODEL_NAME"]

    agent = Agent(
        model_name,
        output_type=PaperAuthors,
        system_prompt=SYSTEM_PROMPT,
        retries=5,
    )

    result = agent.run_sync(paper_text)

    paper_authors = result.output
    paper_authors.arxiv_id = arxiv_id

    return paper_authors
