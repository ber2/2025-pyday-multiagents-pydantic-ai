import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from arxiv_author_affiliation.extractor_agent import extract_authors
from arxiv_author_affiliation.data_models.author import Author
from arxiv_author_affiliation.data_models.affiliation import Affiliation
from arxiv_author_affiliation.data_models.paper_authors import PaperAuthors


TEST_TEXT_PATH = Path(__file__).parent / "resources" / "1706.03762v7.txt"

with open(TEST_TEXT_PATH) as f:
    SAMPLE_TEXT = f.read()


@patch("arxiv_author_affiliation.extractor_agent.Agent")
def test_extract_authors_returns_paper_authors(mock_agent_class):
    mock_agent = Mock()
    mock_agent_class.return_value = mock_agent

    expected_result = PaperAuthors(
        arxiv_id="1706.03762",
        authors=[
            Author(
                name="Ashish Vaswani", affiliations=[Affiliation(name="Google Brain")]
            )
        ],
    )

    mock_run_result = Mock()
    mock_run_result.data = expected_result
    mock_agent.run_sync.return_value = mock_run_result

    result = extract_authors("1706.03762", SAMPLE_TEXT)

    assert isinstance(result, PaperAuthors)
    assert result.arxiv_id == "1706.03762"
    mock_agent.run_sync.assert_called_once()


@patch("arxiv_author_affiliation.extractor_agent.Agent")
def test_extract_authors_calls_agent_with_text(mock_agent_class):
    mock_agent = Mock()
    mock_agent_class.return_value = mock_agent

    expected_result = PaperAuthors(arxiv_id="1706.03762", authors=[])

    mock_run_result = Mock()
    mock_run_result.data = expected_result
    mock_agent.run_sync.return_value = mock_run_result

    extract_authors("1706.03762", SAMPLE_TEXT)

    call_args = mock_agent.run_sync.call_args
    assert SAMPLE_TEXT in str(call_args)


@patch("arxiv_author_affiliation.extractor_agent.Agent")
def test_extract_authors_agent_configured_with_paper_authors_result_type(
    mock_agent_class,
):
    mock_agent = Mock()
    mock_agent_class.return_value = mock_agent

    expected_result = PaperAuthors(arxiv_id="1706.03762", authors=[])

    mock_run_result = Mock()
    mock_run_result.data = expected_result
    mock_agent.run_sync.return_value = mock_run_result

    extract_authors("1706.03762", SAMPLE_TEXT)

    mock_agent_class.assert_called_once()
    call_kwargs = mock_agent_class.call_args.kwargs

    assert "result_type" in call_kwargs
    assert call_kwargs["result_type"] == PaperAuthors


@patch("arxiv_author_affiliation.extractor_agent.Agent")
def test_extract_authors_returns_multiple_authors(mock_agent_class):
    mock_agent = Mock()
    mock_agent_class.return_value = mock_agent

    expected_result = PaperAuthors(
        arxiv_id="1706.03762",
        authors=[
            Author(
                name="Ashish Vaswani", affiliations=[Affiliation(name="Google Brain")]
            ),
            Author(
                name="Noam Shazeer", affiliations=[Affiliation(name="Google Brain")]
            ),
            Author(
                name="Niki Parmar", affiliations=[Affiliation(name="Google Research")]
            ),
        ],
    )

    mock_run_result = Mock()
    mock_run_result.data = expected_result
    mock_agent.run_sync.return_value = mock_run_result

    result = extract_authors("1706.03762", SAMPLE_TEXT)

    assert len(result.authors) == 3
    assert result.authors[0].name == "Ashish Vaswani"
    assert result.authors[1].name == "Noam Shazeer"
