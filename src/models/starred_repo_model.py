from pydantic import BaseModel


class StarredRepoModel(BaseModel):
    """All repos have at least a name, url and topics.
        Other fields can be None (null) if they are missing.
    """
    name: str
    description: str | None
    url: str
    license: dict | None
    topics: list
