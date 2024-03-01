import pytest
from httpx import AsyncClient, ASGITransport
from main import app

# Test the index route with different methods


@pytest.mark.asyncio
async def test_get_index_response_code():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == 307

@pytest.mark.asyncio
async def test_post_index_response_code():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/", json={"data": "some_test_data"})
        assert response.status_code == 405


@pytest.mark.asyncio
async def test_put_index_response_code():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.put("/", json={"data": "some_test_data"})
        assert response.status_code == 405

# Test that the index route creates a GET request


@pytest.mark.asyncio
async def test_get_index_creates_GET_request():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.next_request.method == "GET"

# Test that the index route creates a GET request to the correct URL


@pytest.mark.asyncio
async def test_get_index_creates_GET_request_to_github():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
        authorize_request_url = str(response.next_request.url)
        assert authorize_request_url.startswith(
            "https://github.com/login/oauth/authorize") is True
