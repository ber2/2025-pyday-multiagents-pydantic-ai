from unittest.mock import Mock, patch
from click.testing import CliRunner

from arxiv_author_affiliation.cli import cli
from arxiv_author_affiliation.data_models import ExtractedPaper


@patch('arxiv_author_affiliation.cli.ArxivPDFDownloader')
def test_cli_displays_paper_info(mock_downloader_class):
    mock_downloader = Mock()
    mock_downloader_class.return_value = mock_downloader

    mock_paper = ExtractedPaper(
        arxiv_id="1706.03762",
        text="This is test text with some content.",
        page_count=15
    )
    mock_downloader.download_and_extract.return_value = mock_paper

    runner = CliRunner()
    result = runner.invoke(cli, ["1706.03762"])

    assert result.exit_code == 0
    assert "1706.03762" in result.output
    assert "15" in result.output
    assert "37" in result.output


@patch('arxiv_author_affiliation.cli.ArxivPDFDownloader')
def test_cli_calls_downloader_with_arxiv_id(mock_downloader_class):
    mock_downloader = Mock()
    mock_downloader_class.return_value = mock_downloader

    mock_paper = ExtractedPaper(
        arxiv_id="2301.12345",
        text="Test",
        page_count=10
    )
    mock_downloader.download_and_extract.return_value = mock_paper

    runner = CliRunner()
    result = runner.invoke(cli, ["2301.12345"])

    assert result.exit_code == 0
    mock_downloader.download_and_extract.assert_called_once_with("2301.12345")


def test_cli_requires_arxiv_id():
    runner = CliRunner()
    result = runner.invoke(cli, [])

    assert result.exit_code != 0
    assert "Missing argument" in result.output or "Usage:" in result.output
