from pydantic import BaseModel, Field


class ExtractedPaper(BaseModel):
    arxiv_id: str
    text: str
    page_count: int = Field(gt=0)

    @property
    def text_length(self) -> int:
        return len(self.text)
