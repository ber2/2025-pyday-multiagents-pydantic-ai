import pytest
from pydantic import ValidationError

from arxiv_author_affiliation.data_models import ExtractedPaper


def test_create_extracted_paper():
    paper = ExtractedPaper(
        arxiv_id="2301.12345",
        text="This is the extracted text.",
        page_count=10
    )
    assert paper.arxiv_id == "2301.12345"
    assert paper.text == "This is the extracted text."
    assert paper.page_count == 10


def test_text_length_property():
    paper = ExtractedPaper(
        arxiv_id="2301.12345",
        text="Hello",
        page_count=1
    )
    assert paper.text_length == 5


def test_page_count_must_be_positive():
    with pytest.raises(ValidationError):
        ExtractedPaper(
            arxiv_id="2301.12345",
            text="Some text",
            page_count=0
        )


def test_page_count_cannot_be_negative():
    with pytest.raises(ValidationError):
        ExtractedPaper(
            arxiv_id="2301.12345",
            text="Some text",
            page_count=-1
        )
