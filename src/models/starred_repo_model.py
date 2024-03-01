from pydantic import BaseModel

class StarredRepoModel(BaseModel):
    name: str
    description: str | None
    url: str
    license: dict | None
    topics: list
