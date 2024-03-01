import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_get_index_response_code():
    """A valid GET request should return a 307 status code.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == 307

@pytest.mark.asyncio
async def test_post_index_response_code():
    """The POST request should return a 405 status code.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/", json={"data": "some_test_data"})
        assert response.status_code == 405

@pytest.mark.asyncio
async def test_put_index_response_code():
    """The PUT request should return a 405 status code.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.put("/", json={"data": "some_test_data"})
        assert response.status_code == 405

@pytest.mark.asyncio
async def test_get_index_creates_GET_request():
    """The index route should create a GET request.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.next_request.method == "GET"

@pytest.mark.asyncio
async def test_get_index_creates_GET_request_to_github():
    """The index rpoute should create a GET request to the GitHub OAuth page.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
        authorize_request_url = str(response.next_request.url)
        assert authorize_request_url.startswith(
            "https://github.com/login/oauth/authorize") is True
