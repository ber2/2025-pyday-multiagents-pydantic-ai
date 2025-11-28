import os
from pydantic_ai import Agent

from arxiv_author_affiliation.data_models.affiliation import Affiliation
from arxiv_author_affiliation.data_models.resolver_output import ResolverOutput


SYSTEM_PROMPT = """
You are an expert at validating and normalizing academic institution names.

For each affiliation name provided, you must:
- Determine if it's a real, identifiable institution
- Normalize it to the full, official name (e.g., "MIT" -> "Massachusetts Institute of Technology")
- Assign a confidence score (0.0 to 1.0) for your validation/normalization
- Identify any ambiguous or incomplete affiliations that need clarification

For valid institutions, set is_valid=True and provide the normalized name.
For ambiguous or unidentifiable affiliations, set is_valid=False, needs_clarification=True, and add details to issues.

Return the data in the structured format.
"""


def resolve_affiliations(affiliations: list[Affiliation]) -> ResolverOutput:
    model_name = os.environ["MODEL_NAME"]

    agent = Agent(
        model_name,
        output_type=ResolverOutput,
        system_prompt=SYSTEM_PROMPT,
        retries=5,
    )

    affiliation_names = [aff.name for aff in affiliations]
    affiliation_text = "\n".join(f"- {name}" for name in affiliation_names)

    result = agent.run_sync(f"Affiliations to validate:\n{affiliation_text}")

    return result.output
