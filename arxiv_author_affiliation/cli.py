import click

from arxiv_author_affiliation.pdf_downloader import ArxivPDFDownloader
from arxiv_author_affiliation.extractor_agent import extract_authors


@click.command()
@click.argument("arxiv_id", metavar="ARXIV_ID")
@click.help_option("-h", "--help")
def cli(arxiv_id):
    """
    Download and extract author/affiliation data from an arXiv paper.

    ARXIV_ID: The arXiv paper identifier (e.g., 1706.03762 or 2301.12345v1)
    """
    downloader = ArxivPDFDownloader()
    paper = downloader.download_and_extract(arxiv_id)

    click.echo(f"arXiv ID: {paper.arxiv_id}")
    click.echo(f"Pages: {paper.page_count}")
    click.echo(f"Text length: {paper.text_length}")
    click.echo()

    result = extract_authors(arxiv_id, paper.text)

    click.echo(f"Found {result.author_count} authors:")
    for author in result.authors:
        click.echo(f"  - {author.name}")
        for affiliation in author.affiliations:
            click.echo(f"    * {affiliation.name}")


if __name__ == "__main__":
    cli()
