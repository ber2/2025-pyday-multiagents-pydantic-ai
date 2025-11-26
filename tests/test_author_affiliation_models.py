import pytest
from pydantic import ValidationError

from arxiv_author_affiliation.data_models.author import Author
from arxiv_author_affiliation.data_models.affiliation import Affiliation
from arxiv_author_affiliation.data_models.paper_authors import PaperAuthors


class TestAffiliation:
    def test_create_affiliation_with_name(self):
        affiliation = Affiliation(name="Google Brain")
        assert affiliation.name == "Google Brain"

    def test_affiliation_name_required(self):
        with pytest.raises(ValidationError):
            Affiliation()


class TestAuthor:
    def test_create_author_with_name(self):
        author = Author(name="Ashish Vaswani")
        assert author.name == "Ashish Vaswani"

    def test_create_author_with_affiliations(self):
        affiliations = [
            Affiliation(name="Google Brain"),
            Affiliation(name="Google Research"),
        ]
        author = Author(name="Ashish Vaswani", affiliations=affiliations)
        assert author.name == "Ashish Vaswani"
        assert len(author.affiliations) == 2
        assert author.affiliations[0].name == "Google Brain"

    def test_author_name_required(self):
        with pytest.raises(ValidationError):
            Author()

    def test_author_affiliations_defaults_to_empty_list(self):
        author = Author(name="John Doe")
        assert author.affiliations == []


class TestPaperAuthors:
    def test_create_paper_authors_with_arxiv_id_and_authors(self):
        authors = [
            Author(
                name="Ashish Vaswani", affiliations=[Affiliation(name="Google Brain")]
            ),
            Author(
                name="Noam Shazeer", affiliations=[Affiliation(name="Google Brain")]
            ),
        ]
        paper = PaperAuthors(arxiv_id="1706.03762", authors=authors)
        assert paper.arxiv_id == "1706.03762"
        assert len(paper.authors) == 2

    def test_paper_authors_arxiv_id_required(self):
        with pytest.raises(ValidationError):
            PaperAuthors(authors=[])

    def test_paper_authors_authors_required(self):
        with pytest.raises(ValidationError):
            PaperAuthors(arxiv_id="1706.03762")

    def test_paper_authors_count_property(self):
        authors = [
            Author(name="Author 1", affiliations=[]),
            Author(name="Author 2", affiliations=[]),
            Author(name="Author 3", affiliations=[]),
        ]
        paper = PaperAuthors(arxiv_id="1706.03762", authors=authors)
        assert paper.author_count == 3
