import click

from arxiv_author_affiliation.pdf_downloader import ArxivPDFDownloader


@click.command()
@click.argument('arxiv_id', metavar='ARXIV_ID')
@click.help_option('-h', '--help')
def cli(arxiv_id):
    """
    Download and extract metadata from an arXiv paper.

    ARXIV_ID: The arXiv paper identifier (e.g., 1706.03762 or 2301.12345v1)
    """
    downloader = ArxivPDFDownloader()
    paper = downloader.download_and_extract(arxiv_id)

    click.echo(f"arXiv ID: {paper.arxiv_id}")
    click.echo(f"Pages: {paper.page_count}")
    click.echo(f"Text length: {paper.text_length}")


def main():
    cli()


if __name__ == "__main__":
    main()
