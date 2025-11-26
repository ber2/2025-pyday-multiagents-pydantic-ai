from pydantic import BaseModel


class Affiliation(BaseModel):
    name: str
