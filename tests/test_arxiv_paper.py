import pytest
from pydantic import ValidationError

from arxiv_author_affiliation.data_models import ArxivPaper


def test_valid_arxiv_id():
    paper = ArxivPaper(arxiv_id="2301.12345")
    assert paper.arxiv_id == "2301.12345"


def test_valid_arxiv_id_with_version():
    paper = ArxivPaper(arxiv_id="2301.12345v1")
    assert paper.arxiv_id == "2301.12345v1"


def test_valid_older_format():
    paper = ArxivPaper(arxiv_id="1706.03762")
    assert paper.arxiv_id == "1706.03762"


def test_empty_arxiv_id_raises_error():
    with pytest.raises(ValidationError):
        ArxivPaper(arxiv_id="")


def test_invalid_format_no_dot_raises_error():
    with pytest.raises(ValidationError):
        ArxivPaper(arxiv_id="230112345")


def test_invalid_format_non_numeric_raises_error():
    with pytest.raises(ValidationError):
        ArxivPaper(arxiv_id="abcd.12345")


def test_invalid_format_too_many_parts_raises_error():
    with pytest.raises(ValidationError):
        ArxivPaper(arxiv_id="2301.123.45")
