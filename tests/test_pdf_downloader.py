import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from pydantic import ValidationError

from arxiv_author_affiliation.pdf_downloader import ArxivPDFDownloader


TEST_ARXIV_ID = "1706.03762"
TEST_PDF_PATH = Path(__file__).parent / "resources" / "1706.03762v7.pdf"


def test_downloader_creates_cache_dir(tmp_path):
    cache_dir = tmp_path / "test_cache"
    downloader = ArxivPDFDownloader(cache_dir=cache_dir)
    assert cache_dir.exists()
    assert cache_dir.is_dir()


def test_download_validates_arxiv_id(tmp_path):
    downloader = ArxivPDFDownloader(cache_dir=tmp_path)
    with pytest.raises(ValidationError):
        downloader.download_and_extract("invalid-id")


@patch("httpx.get")
def test_downloads_pdf_to_cache_dir(mock_get, tmp_path):
    with open(TEST_PDF_PATH, "rb") as f:
        pdf_content = f.read()

    mock_response = Mock()
    mock_response.content = pdf_content
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    downloader = ArxivPDFDownloader(cache_dir=tmp_path)
    downloader.download_and_extract(TEST_ARXIV_ID)

    expected_url = f"https://arxiv.org/pdf/{TEST_ARXIV_ID}.pdf"
    mock_get.assert_called_once_with(expected_url, follow_redirects=True)
    mock_response.raise_for_status.assert_called_once()

    expected_pdf_path = tmp_path / f"{TEST_ARXIV_ID}.pdf"
    assert expected_pdf_path.exists()


@patch("httpx.get")
def test_extracts_text_from_pdf(mock_get, tmp_path):
    with open(TEST_PDF_PATH, "rb") as f:
        pdf_content = f.read()

    mock_response = Mock()
    mock_response.content = pdf_content
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    downloader = ArxivPDFDownloader(cache_dir=tmp_path)
    result = downloader.download_and_extract(TEST_ARXIV_ID)

    expected_url = f"https://arxiv.org/pdf/{TEST_ARXIV_ID}.pdf"
    mock_get.assert_called_once_with(expected_url, follow_redirects=True)
    mock_response.raise_for_status.assert_called_once()

    assert result.arxiv_id == TEST_ARXIV_ID
    assert len(result.text) > 0
    assert "Attention" in result.text
    assert result.page_count > 0


@patch("httpx.get")
def test_uses_cached_pdf_if_exists(mock_get, tmp_path):
    with open(TEST_PDF_PATH, "rb") as f:
        pdf_content = f.read()

    cached_pdf = tmp_path / f"{TEST_ARXIV_ID}.pdf"
    cached_pdf.write_bytes(pdf_content)

    downloader = ArxivPDFDownloader(cache_dir=tmp_path)
    result = downloader.download_and_extract(TEST_ARXIV_ID)

    mock_get.assert_not_called()
    assert result.arxiv_id == TEST_ARXIV_ID
    assert len(result.text) > 0


@patch("httpx.get")
def test_follows_redirects(mock_get, tmp_path):
    with open(TEST_PDF_PATH, "rb") as f:
        pdf_content = f.read()

    mock_response = Mock()
    mock_response.content = pdf_content
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    downloader = ArxivPDFDownloader(cache_dir=tmp_path)
    result = downloader.download_and_extract(TEST_ARXIV_ID)

    expected_url = f"https://arxiv.org/pdf/{TEST_ARXIV_ID}.pdf"
    mock_get.assert_called_once_with(expected_url, follow_redirects=True)
    mock_response.raise_for_status.assert_called_once()

    assert result.arxiv_id == TEST_ARXIV_ID
    assert len(result.text) > 0
