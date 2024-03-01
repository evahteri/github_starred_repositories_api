import pytest
from fastapi import HTTPException
from main import get_repositories


@pytest.mark.asyncio
async def test_get_repositories():
    """The function should raise a http exception with status code 401
    with details, if the token is invalid."""
    token = "1234567890"

    with pytest.raises(HTTPException) as error:
        await get_repositories(token)
    assert error.value.status_code == 401
    assert error.value.detail == "Unable to reach the resource. Recheck parameters"
