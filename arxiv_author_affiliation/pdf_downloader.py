from pathlib import Path

import httpx
import pymupdf

from arxiv_author_affiliation.data_models.arxiv_paper import ArxivPaper
from arxiv_author_affiliation.data_models.extracted_paper import ExtractedPaper


class ArxivPDFDownloader:
    def __init__(self, cache_dir: Path | None = None):
        self.cache_dir = cache_dir or Path.cwd() / ".arxiv_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def download_and_extract(self, arxiv_id: str) -> ExtractedPaper:
        paper = ArxivPaper(arxiv_id=arxiv_id)
        pdf_path = self._get_or_download_pdf(paper.arxiv_id)
        text, page_count = self._extract_text_from_pdf(pdf_path)

        return ExtractedPaper(arxiv_id=paper.arxiv_id, text=text, page_count=page_count)

    def _get_or_download_pdf(self, arxiv_id: str) -> Path:
        pdf_path = self.cache_dir / f"{arxiv_id}.pdf"

        if pdf_path.exists():
            return pdf_path

        url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        response = httpx.get(url, follow_redirects=True)
        response.raise_for_status()

        pdf_path.write_bytes(response.content)
        return pdf_path

    def _extract_text_from_pdf(self, pdf_path: Path) -> tuple[str, int]:
        doc = pymupdf.open(pdf_path)
        page_count = len(doc)

        text_parts = []
        for page in doc:
            text_parts.append(page.get_text())

        full_text = "\n".join(text_parts)
        doc.close()

        return full_text, page_count
