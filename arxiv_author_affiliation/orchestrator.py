from arxiv_author_affiliation.extractor_agent import extract_authors
from arxiv_author_affiliation.resolver_agent import resolve_affiliations
from arxiv_author_affiliation.data_models.validated_paper import ValidatedPaper


def process_paper(arxiv_id: str, paper_text: str) -> ValidatedPaper:
    paper_authors = extract_authors(arxiv_id, paper_text)

    all_affiliations = []
    for author in paper_authors.authors:
        all_affiliations.extend(author.affiliations)

    unique_affiliations = []
    seen_names = set()
    for affiliation in all_affiliations:
        if affiliation.name not in seen_names:
            unique_affiliations.append(affiliation)
            seen_names.add(affiliation.name)

    resolver_output = resolve_affiliations(unique_affiliations)

    validation_issues = resolver_output.issues if resolver_output.issues else []

    return ValidatedPaper(
        arxiv_id=arxiv_id,
        authors=paper_authors.authors,
        normalized_affiliations=resolver_output.normalized_affiliations,
        validation_issues=validation_issues,
    )
