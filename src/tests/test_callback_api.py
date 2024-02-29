import pytest
from httpx import AsyncClient, ASGITransport
from main import app
import session

session.ENVIRONMENT = "test"

@pytest.mark.asyncio
async def test_get_callback_response_code_different_states():
    session.SESSION_SECRET = "this_is_a_secret"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/callback", params={"code": "12n3poi3102", "state": "this_is_not_the_same_secret"})
        assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_callback_response_no_parameters():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/callback")
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_callback_response_parameters_null():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/callback", params={"code": "", "state": ""})
        assert response.status_code == 422
    
@pytest.mark.asyncio
async def test_get_callback_response_code_correct_state_incorrect_code():
    session.SESSION_SECRET = "this_is_a_secret"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/callback", params={"code": "12n3poi3102", "state": "this_is_a_secret"})
        assert response.status_code == 401
        assert response.json() == {"detail": "Unauthorized. The code passed is incorrect or expired"}

@pytest.mark.asyncio
async def test_get_callback_response_code_correct_state_creates_POST_request():
    """Test that the callback route creates a POST request to the correct URL.
    Github api will answer with an error, because client id, client secret and code are not valid.
    """
    session.SESSION_SECRET = "this_is_a_secret"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/callback", params={"code": "12n3poi3102", "state": "this_is_a_secret"})
        assert response.json() == {"detail": "Unauthorized. The code passed is incorrect or expired"}
