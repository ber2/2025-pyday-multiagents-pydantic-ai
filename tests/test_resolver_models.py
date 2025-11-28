import pytest
from pydantic import ValidationError

from arxiv_author_affiliation.data_models.normalized_affiliation import (
    NormalizedAffiliation,
)
from arxiv_author_affiliation.data_models.resolver_output import ResolverOutput


class TestNormalizedAffiliation:
    def test_normalized_affiliation_has_required_fields(self):
        affiliation = NormalizedAffiliation(
            original_name="MIT",
            normalized_name="Massachusetts Institute of Technology",
            is_valid=True,
            confidence=0.95,
        )

        assert affiliation.original_name == "MIT"
        assert affiliation.normalized_name == "Massachusetts Institute of Technology"
        assert affiliation.is_valid is True
        assert affiliation.confidence == 0.95

    def test_normalized_affiliation_requires_all_fields(self):
        with pytest.raises(ValidationError):
            NormalizedAffiliation(original_name="MIT")

    def test_normalized_affiliation_confidence_is_float(self):
        affiliation = NormalizedAffiliation(
            original_name="Stanford",
            normalized_name="Stanford University",
            is_valid=True,
            confidence=0.88,
        )

        assert isinstance(affiliation.confidence, float)

    def test_normalized_affiliation_can_be_invalid(self):
        affiliation = NormalizedAffiliation(
            original_name="Unknown Corp",
            normalized_name="Unknown Corp",
            is_valid=False,
            confidence=0.2,
        )

        assert affiliation.is_valid is False


class TestResolverOutput:
    def test_resolver_output_with_valid_affiliations(self):
        output = ResolverOutput(
            normalized_affiliations=[
                NormalizedAffiliation(
                    original_name="MIT",
                    normalized_name="Massachusetts Institute of Technology",
                    is_valid=True,
                    confidence=0.95,
                )
            ],
            needs_clarification=False,
            issues=[],
        )

        assert len(output.normalized_affiliations) == 1
        assert output.needs_clarification is False
        assert len(output.issues) == 0

    def test_resolver_output_with_issues(self):
        output = ResolverOutput(
            normalized_affiliations=[],
            needs_clarification=True,
            issues=["Ambiguous affiliation: ABC Research"],
        )

        assert output.needs_clarification is True
        assert len(output.issues) == 1
        assert "Ambiguous" in output.issues[0]

    def test_resolver_output_needs_clarification_defaults_to_false(self):
        output = ResolverOutput(normalized_affiliations=[])

        assert output.needs_clarification is False

    def test_resolver_output_issues_defaults_to_empty_list(self):
        output = ResolverOutput(normalized_affiliations=[])

        assert output.issues == []

    def test_resolver_output_can_have_multiple_affiliations(self):
        output = ResolverOutput(
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
            ]
        )

        assert len(output.normalized_affiliations) == 2
