from unittest.mock import patch
from pathlib import Path

from arxiv_author_affiliation.orchestrator import process_paper
from arxiv_author_affiliation.data_models.author import Author
from arxiv_author_affiliation.data_models.affiliation import Affiliation
from arxiv_author_affiliation.data_models.paper_authors import PaperAuthors
from arxiv_author_affiliation.data_models.normalized_affiliation import (
    NormalizedAffiliation,
)
from arxiv_author_affiliation.data_models.resolver_output import ResolverOutput
from arxiv_author_affiliation.data_models.validated_paper import ValidatedPaper


TEST_TEXT_PATH = Path(__file__).parent / "resources" / "1706.03762v7.txt"

with open(TEST_TEXT_PATH) as f:
    SAMPLE_TEXT = f.read()


@patch("arxiv_author_affiliation.orchestrator.resolve_affiliations")
@patch("arxiv_author_affiliation.orchestrator.extract_authors")
def test_orchestrator_calls_extractor_first(mock_extract, mock_resolve):
    mock_extract.return_value = PaperAuthors(
        arxiv_id="1706.03762",
        authors=[Author(name="Test Author", affiliations=[Affiliation(name="MIT")])],
    )
    mock_resolve.return_value = ResolverOutput(
        normalized_affiliations=[
            NormalizedAffiliation(
                original_name="MIT",
                normalized_name="Massachusetts Institute of Technology",
                is_valid=True,
                confidence=0.95,
            )
        ]
    )

    process_paper("1706.03762", SAMPLE_TEXT)

    mock_extract.assert_called_once_with("1706.03762", SAMPLE_TEXT)


@patch("arxiv_author_affiliation.orchestrator.resolve_affiliations")
@patch("arxiv_author_affiliation.orchestrator.extract_authors")
def test_orchestrator_calls_resolver_with_extracted_affiliations(
    mock_extract, mock_resolve
):
    mock_extract.return_value = PaperAuthors(
        arxiv_id="1706.03762",
        authors=[Author(name="Test Author", affiliations=[Affiliation(name="MIT")])],
    )
    mock_resolve.return_value = ResolverOutput(
        normalized_affiliations=[
            NormalizedAffiliation(
                original_name="MIT",
                normalized_name="Massachusetts Institute of Technology",
                is_valid=True,
                confidence=0.95,
            )
        ]
    )

    process_paper("1706.03762", SAMPLE_TEXT)

    mock_resolve.assert_called_once()
    call_args = mock_resolve.call_args[0][0]

    # Should pass all unique affiliations to resolver
    assert isinstance(call_args, list)
    assert len(call_args) > 0
    assert all(isinstance(aff, Affiliation) for aff in call_args)


@patch("arxiv_author_affiliation.orchestrator.resolve_affiliations")
@patch("arxiv_author_affiliation.orchestrator.extract_authors")
def test_orchestrator_returns_validated_paper(mock_extract, mock_resolve):
    mock_extract.return_value = PaperAuthors(
        arxiv_id="1706.03762",
        authors=[Author(name="Test Author", affiliations=[Affiliation(name="MIT")])],
    )
    mock_resolve.return_value = ResolverOutput(
        normalized_affiliations=[
            NormalizedAffiliation(
                original_name="MIT",
                normalized_name="Massachusetts Institute of Technology",
                is_valid=True,
                confidence=0.95,
            )
        ]
    )

    result = process_paper("1706.03762", SAMPLE_TEXT)

    assert isinstance(result, ValidatedPaper)
    assert result.arxiv_id == "1706.03762"


@patch("arxiv_author_affiliation.orchestrator.resolve_affiliations")
@patch("arxiv_author_affiliation.orchestrator.extract_authors")
def test_orchestrator_includes_normalized_affiliations_in_result(
    mock_extract, mock_resolve
):
    mock_extract.return_value = PaperAuthors(
        arxiv_id="1706.03762",
        authors=[Author(name="Test Author", affiliations=[Affiliation(name="MIT")])],
    )

    normalized = NormalizedAffiliation(
        original_name="MIT",
        normalized_name="Massachusetts Institute of Technology",
        is_valid=True,
        confidence=0.95,
    )

    mock_resolve.return_value = ResolverOutput(normalized_affiliations=[normalized])

    result = process_paper("1706.03762", SAMPLE_TEXT)

    assert hasattr(result, "authors")
    assert len(result.authors) > 0
    assert hasattr(result, "normalized_affiliations")
    assert len(result.normalized_affiliations) == 1
    assert result.normalized_affiliations[0].original_name == "MIT"
    assert result.normalized_affiliations[0].normalized_name == "Massachusetts Institute of Technology"


@patch("arxiv_author_affiliation.orchestrator.resolve_affiliations")
@patch("arxiv_author_affiliation.orchestrator.extract_authors")
def test_orchestrator_handles_resolver_issues(mock_extract, mock_resolve):
    mock_extract.return_value = PaperAuthors(
        arxiv_id="1706.03762",
        authors=[
            Author(name="Test Author", affiliations=[Affiliation(name="Unknown Lab")])
        ],
    )

    mock_resolve.return_value = ResolverOutput(
        normalized_affiliations=[],
        needs_clarification=True,
        issues=["Ambiguous affiliation: Unknown Lab"],
    )

    result = process_paper("1706.03762", SAMPLE_TEXT)

    assert isinstance(result, ValidatedPaper)
    assert len(result.validation_issues) > 0
    assert (
        "Unknown Lab" in result.validation_issues[0]
        or "Ambiguous" in result.validation_issues[0]
    )


@patch("arxiv_author_affiliation.orchestrator.resolve_affiliations")
@patch("arxiv_author_affiliation.orchestrator.extract_authors")
def test_orchestrator_extracts_unique_affiliations(mock_extract, mock_resolve):
    # Same affiliation appears multiple times across authors
    mock_extract.return_value = PaperAuthors(
        arxiv_id="1706.03762",
        authors=[
            Author(name="Author 1", affiliations=[Affiliation(name="MIT")]),
            Author(name="Author 2", affiliations=[Affiliation(name="MIT")]),
            Author(name="Author 3", affiliations=[Affiliation(name="Stanford")]),
        ],
    )

    mock_resolve.return_value = ResolverOutput(normalized_affiliations=[])

    process_paper("1706.03762", SAMPLE_TEXT)

    call_args = mock_resolve.call_args[0][0]
    affiliation_names = [aff.name for aff in call_args]

    # Should only pass unique affiliations to resolver
    assert len(affiliation_names) == len(set(affiliation_names))
    assert "MIT" in affiliation_names
    assert "Stanford" in affiliation_names


@patch("arxiv_author_affiliation.orchestrator.resolve_affiliations")
@patch("arxiv_author_affiliation.orchestrator.extract_authors")
def test_orchestrator_handles_multiple_authors(mock_extract, mock_resolve):
    mock_extract.return_value = PaperAuthors(
        arxiv_id="1706.03762",
        authors=[
            Author(name="Author 1", affiliations=[Affiliation(name="MIT")]),
            Author(name="Author 2", affiliations=[Affiliation(name="Stanford")]),
            Author(name="Author 3", affiliations=[Affiliation(name="Berkeley")]),
        ],
    )

    mock_resolve.return_value = ResolverOutput(
        normalized_affiliations=[
            NormalizedAffiliation(
                original_name="MIT",
                normalized_name="Massachusetts Institute of Technology",
                is_valid=True,
                confidence=0.95,
            ),
            NormalizedAffiliation(
                original_name="Stanford",
                normalized_name="Stanford University",
                is_valid=True,
                confidence=0.92,
            ),
            NormalizedAffiliation(
                original_name="Berkeley",
                normalized_name="University of California, Berkeley",
                is_valid=True,
                confidence=0.93,
            ),
        ]
    )

    result = process_paper("1706.03762", SAMPLE_TEXT)

    assert len(result.authors) == 3
    assert len(result.normalized_affiliations) == 3
    normalized_names = [aff.normalized_name for aff in result.normalized_affiliations]
    assert "Massachusetts Institute of Technology" in normalized_names
    assert "Stanford University" in normalized_names
    assert "University of California, Berkeley" in normalized_names
