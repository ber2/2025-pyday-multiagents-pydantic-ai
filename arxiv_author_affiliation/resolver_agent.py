from pydantic_ai import Agent

from arxiv_author_affiliation.data_models.affiliation import Affiliation
from arxiv_author_affiliation.data_models.resolver_output import ResolverOutput


def resolve_affiliations(affiliations: list[Affiliation]) -> ResolverOutput:
    pass
