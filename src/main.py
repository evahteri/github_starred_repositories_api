from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from services.random_string_generator import RandomStringGenerator
from dotenv import dotenv_values
from services.config_validator import ConfigValidator
from services.starred_repos_parser import StarredReposParser
import session
import configuration
import test_configuration
import httpx
import uvicorn

app = FastAPI()
client_id = configuration.CLIENT_ID
client_secret = configuration.CLIENT_SECRET
if session.ENVIRONMENT == "test":
    client_id = test_configuration.CLIENT_ID
    client_secret = test_configuration.CLIENT_SECRET

@app.get("/callback")
async def callback(code:str, state: str):
    if len(code) < 1 or len(state) < 1:
        raise HTTPException(status_code=422, detail="Unprocessable Entity. Invalid parameters")
    if state != session.SESSION_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized. Invalid session token")
    async with httpx.AsyncClient() as client:
        headers = {
            "Accept": "application/json"
        }
        auth_data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code
        }
        oauth_response = await client.post(f"https://github.com/login/oauth/access_token", json=auth_data, headers=headers)
        if "error" in oauth_response.json() or oauth_response.status_code != 200:
            raise HTTPException(401, detail="Unauthorized. The code passed is incorrect or expired")
        try:
            access_token = oauth_response.json()["access_token"]
            return await get_repositories(token=access_token)
        except KeyError:
            raise HTTPException(401, detail="Unauthorized. The code passed is incorrect or expired")

@app.get("/")
async def index():
    """Redirects to GitHub's OAuth page for user authentication.
    Using public_repo scope for read-only access to public repositories.
    Creating a random session state secret to prevent CSRF attacks.
    """
    session.SESSION_SECRET = RandomStringGenerator().generate_random_string(45)
    scope = "public_repo"
    state=session.SESSION_SECRET
    async with httpx.AsyncClient() as client:
        params = {
        "scope": scope,
        "state": state,
        "client_id": client_id
        }
        response = await client.get(f"https://github.com/login/oauth/authorize", params=params)
        if response.status_code != 302:
            raise HTTPException(status_code=404, detail="Unable to reach authentication page. Recheck parameters")
        return RedirectResponse(response.url)

async def get_repositories(token:str):
    async with httpx.AsyncClient() as client:
        headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + token,
        "X-GitHub-Api-Version": "2022-11-28"
        }
        starred_repositories = await client.get(f"https://api.github.com/user/starred", headers=headers)
        if starred_repositories.status_code != 200:
            raise HTTPException(status_code=starred_repositories.status_code, detail="Unable to reach the resource. Recheck parameters")
        return StarredReposParser(starred_repos=starred_repositories.json()).get_starred_repos_response()

if __name__ == "__main__":
    if not ConfigValidator(client_id=client_id, client_secret=client_secret).validate_secrets():
        raise ValueError("Invalid configuration. Follow instructions in README to configure the application")
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)