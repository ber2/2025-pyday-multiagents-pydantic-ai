from unittest.mock import Mock, patch

from arxiv_author_affiliation.resolver_agent import resolve_affiliations
from arxiv_author_affiliation.data_models.affiliation import Affiliation
from arxiv_author_affiliation.data_models.normalized_affiliation import NormalizedAffiliation
from arxiv_author_affiliation.data_models.resolver_output import ResolverOutput


@patch.dict("os.environ", {"MODEL_NAME": "gemini-1.5-flash"})
@patch("arxiv_author_affiliation.resolver_agent.Agent")
def test_resolve_affiliations_returns_resolver_output(mock_agent_class):
    mock_agent = Mock()
    mock_agent_class.return_value = mock_agent

    expected_result = ResolverOutput(
        normalized_affiliations=[
            NormalizedAffiliation(
                original_name="MIT",
                normalized_name="Massachusetts Institute of Technology",
                is_valid=True,
                confidence=0.95
            )
        ],
        needs_clarification=False,
        issues=[]
    )

    mock_run_result = Mock()
    mock_run_result.output = expected_result
    mock_agent.run_sync.return_value = mock_run_result

    affiliations = [Affiliation(name="MIT")]
    result = resolve_affiliations(affiliations)

    assert isinstance(result, ResolverOutput)
    assert len(result.normalized_affiliations) == 1
    assert result.normalized_affiliations[0].normalized_name == "Massachusetts Institute of Technology"


@patch.dict("os.environ", {"MODEL_NAME": "gemini-1.5-flash"})
@patch("arxiv_author_affiliation.resolver_agent.Agent")
def test_resolve_affiliations_configured_with_resolver_output_type(mock_agent_class):
    mock_agent = Mock()
    mock_agent_class.return_value = mock_agent

    expected_result = ResolverOutput(normalized_affiliations=[])
    mock_run_result = Mock()
    mock_run_result.output = expected_result
    mock_agent.run_sync.return_value = mock_run_result

    affiliations = [Affiliation(name="MIT")]
    resolve_affiliations(affiliations)

    mock_agent_class.assert_called_once()
    call_kwargs = mock_agent_class.call_args.kwargs

    assert "output_type" in call_kwargs
    assert call_kwargs["output_type"] == ResolverOutput


@patch.dict("os.environ", {"MODEL_NAME": "gemini-1.5-flash"})
@patch("arxiv_author_affiliation.resolver_agent.Agent")
def test_resolve_affiliations_passes_affiliation_names_to_agent(mock_agent_class):
    mock_agent = Mock()
    mock_agent_class.return_value = mock_agent

    expected_result = ResolverOutput(normalized_affiliations=[])
    mock_run_result = Mock()
    mock_run_result.output = expected_result
    mock_agent.run_sync.return_value = mock_run_result

    affiliations = [
        Affiliation(name="MIT"),
        Affiliation(name="Stanford")
    ]
    resolve_affiliations(affiliations)

    mock_agent.run_sync.assert_called_once()
    call_args = mock_agent.run_sync.call_args[0][0]

    assert "MIT" in call_args
    assert "Stanford" in call_args


@patch.dict("os.environ", {"MODEL_NAME": "gemini-1.5-flash"})
@patch("arxiv_author_affiliation.resolver_agent.Agent")
def test_resolve_affiliations_detects_issues(mock_agent_class):
    mock_agent = Mock()
    mock_agent_class.return_value = mock_agent

    expected_result = ResolverOutput(
        normalized_affiliations=[],
        needs_clarification=True,
        issues=["Ambiguous affiliation: Unknown Research Lab"]
    )

    mock_run_result = Mock()
    mock_run_result.output = expected_result
    mock_agent.run_sync.return_value = mock_run_result

    affiliations = [Affiliation(name="Unknown Research Lab")]
    result = resolve_affiliations(affiliations)

    assert result.needs_clarification is True
    assert len(result.issues) > 0


@patch.dict("os.environ", {"MODEL_NAME": "gemini-1.5-flash"})
@patch("arxiv_author_affiliation.resolver_agent.Agent")
def test_resolve_affiliations_handles_multiple_affiliations(mock_agent_class):
    mock_agent = Mock()
    mock_agent_class.return_value = mock_agent

    expected_result = ResolverOutput(
        normalized_affiliations=[
            NormalizedAffiliation(
                original_name="MIT",
                normalized_name="Massachusetts Institute of Technology",
                is_valid=True,
                confidence=0.95
            ),
            NormalizedAffiliation(
                original_name="Stanford",
                normalized_name="Stanford University",
                is_valid=True,
                confidence=0.92
            )
        ]
    )

    mock_run_result = Mock()
    mock_run_result.output = expected_result
    mock_agent.run_sync.return_value = mock_run_result

    affiliations = [
        Affiliation(name="MIT"),
        Affiliation(name="Stanford")
    ]
    result = resolve_affiliations(affiliations)

    assert len(result.normalized_affiliations) == 2


@patch.dict("os.environ", {"MODEL_NAME": "gemini-1.5-flash"})
@patch("arxiv_author_affiliation.resolver_agent.Agent")
def test_resolve_affiliations_has_system_prompt(mock_agent_class):
    mock_agent = Mock()
    mock_agent_class.return_value = mock_agent

    expected_result = ResolverOutput(normalized_affiliations=[])
    mock_run_result = Mock()
    mock_run_result.output = expected_result
    mock_agent.run_sync.return_value = mock_run_result

    affiliations = [Affiliation(name="MIT")]
    resolve_affiliations(affiliations)

    mock_agent_class.assert_called_once()
    call_kwargs = mock_agent_class.call_args.kwargs

    assert "system_prompt" in call_kwargs
    assert isinstance(call_kwargs["system_prompt"], str)
    assert len(call_kwargs["system_prompt"]) > 0
