from pydantic import BaseModel, Field, field_validator


class ArxivPaper(BaseModel):
    arxiv_id: str = Field(
        ...,
        description="arXiv paper ID (e.g., '2301.12345' or '2301.12345v1')",
        examples=["2301.12345", "2301.12345v1", "1706.03762"],
    )

    @field_validator("arxiv_id")
    @classmethod
    def validate_arxiv_id(cls, v: str) -> str:
        if not v:
            raise ValueError("arXiv ID cannot be empty")

        base_id = v.split("v")[0]
        parts = base_id.split(".")

        if len(parts) != 2:
            raise ValueError(f"Invalid arXiv ID format: {v}")

        if not parts[0].isdigit() or not parts[1].isdigit():
            raise ValueError(f"Invalid arXiv ID format: {v}")

        return v
