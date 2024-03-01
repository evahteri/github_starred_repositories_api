from pydantic import BaseModel


class StarredRepoModel(BaseModel):
    """Model for the starred repository.
    """
    name: str
    description: str | None
    url: str
    license: dict | None
    topics: list
