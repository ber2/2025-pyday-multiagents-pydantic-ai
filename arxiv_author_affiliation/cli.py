import os
import click
from dotenv import load_dotenv

import logfire

from arxiv_author_affiliation.pdf_downloader import ArxivPDFDownloader
from arxiv_author_affiliation.extractor_agent import extract_authors


load_dotenv()

if logfire_token := os.getenv("LOGFIRE_TOKEN"):
    logfire.configure(token=logfire_token)
logfire.instrument_pydantic_ai()


@click.command()
@click.argument("arxiv_id", metavar="ARXIV_ID")
@click.help_option("-h", "--help")
def cli(arxiv_id):
    """
    Download and extract author/affiliation data from an arXiv paper.

    ARXIV_ID: The arXiv paper identifier (e.g., 1706.03762 or 2301.12345v1)
    """
    with logfire.span("extract_arxiv_authors", arxiv_id=arxiv_id):
        downloader = ArxivPDFDownloader()
        paper = downloader.download_and_extract(arxiv_id)

        logfire.info(f"arXiv ID: {paper.arxiv_id}")
        logfire.info(f"Pages: {paper.page_count}")
        logfire.info(f"Text length: {paper.text_length}")

        result = extract_authors(arxiv_id, paper.text)

        logfire.info(f"Found {result.author_count} authors:")
        for author in result.authors:
            logfire.info(f"  - {author.name}")
            for affiliation in author.affiliations:
                logfire.info(f"    * {affiliation.name}")


if __name__ == "__main__":
    cli()
