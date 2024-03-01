import httpx
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import session
import configuration
from services.random_string_generator import RandomStringGenerator
from services.config_validator import ConfigValidator
from services.starred_repos_parser import StarredReposParser

app = FastAPI()
CLIENT_ID = configuration.CLIENT_ID
CLIENT_SECRET = configuration.CLIENT_SECRET


@app.get("/callback")
async def callback(code: str, state: str):
    """Callback route to handle the response from GitHub's OAuth page.
    If the code and state are valid, it will fetch an access token from GitHub's API and pass it
    to the get_repositories function to fetch the user's starred repositories.
    Args:
        code (str): The code returned by GitHub's OAuth page
        state (str): The state returned by GitHub's OAuth page. 
        Should match the local session state secret
    """
    if len(code) < 1 or len(state) < 1:
        raise HTTPException(
            status_code=422, detail="Unprocessable Entity. Invalid parameters")
    if state != session.SESSION_SECRET:
        raise HTTPException(
            status_code=401, detail="Unauthorized. Invalid session token")
    async with httpx.AsyncClient() as client:
        headers = {
            "Accept": "application/json"
        }
        auth_data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code
        }
        oauth_response = await client.post("https://github.com/login/oauth/access_token",
                                           json=auth_data, headers=headers)
        if "error" in oauth_response.json() or oauth_response.status_code != 200:
            raise HTTPException(
                401, detail="Unauthorized. The code passed is incorrect or expired")
        try:
            access_token = oauth_response.json()["access_token"]
            return await get_repositories(token=access_token)
        except KeyError:
            raise HTTPException(
                401, detail="Unauthorized. The code passed is incorrect or expired")


@app.get("/")
async def index():
    """Redirects to GitHub's OAuth page for user authentication.
    Using public_repo scope for read-only access to public repositories.
    Creating a random session state secret to prevent CSRF attacks.
    """
    session.SESSION_SECRET = RandomStringGenerator().generate_random_string(45)
    scope = "public_repo"
    state = session.SESSION_SECRET
    async with httpx.AsyncClient() as client:
        params = {
            "scope": scope,
            "state": state,
            "client_id": CLIENT_ID
        }
        response = await client.get("https://github.com/login/oauth/authorize", params=params)
        if response.status_code != 302:
            raise HTTPException(
                status_code=404, detail="Unable to reach authentication page. Recheck parameters")
        return RedirectResponse(response.url)


async def get_repositories(token: str):
    """Function get starred repositories from GitHub's API using the provided access token.

    Args:
        token (str): Unique access token for the user

    Returns:
        json: A JSON response containing the number of user's starred repositories and their info   
        """
    async with httpx.AsyncClient() as client:
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + token,
            "X-GitHub-Api-Version": "2022-11-28"
        }
        starred_repositories_response = await client.get("https://api.github.com/user/starred",
                                                         headers=headers)
        if starred_repositories_response.status_code != 200:
            raise HTTPException(status_code=starred_repositories_response.status_code,
                                detail="Unable to reach the resource. Recheck parameters")
        return StarredReposParser(starred_repos=starred_repositories_response.json()
                                  ).get_starred_repos_response()

if __name__ == "__main__":
    CLIENT_ID = configuration.CLIENT_ID
    CLIENT_SECRET = configuration.CLIENT_SECRET
    if not ConfigValidator(client_id=CLIENT_ID, client_secret=CLIENT_SECRET).validate_secrets():
        raise ValueError(
            "Invalid configuration. Follow instructions in README to configure the application")
    uvicorn.run(app, host="0.0.0.0", port=8000)
