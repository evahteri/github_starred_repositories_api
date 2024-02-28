from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from services.random_string_generator import RandomStringGenerator
from dotenv import dotenv_values
from services.config_validator import ConfigValidator
import session_state
import configuration
import httpx
import uvicorn

app = FastAPI()    
client_id = configuration.CLIENT_ID
client_secret = configuration.CLIENT_SECRET

@app.get("/callback")
async def callback(code:str, state: str):
    if state != session_state.SESSION_SECRET:
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
        oauth_access_token = await client.post(f"https://github.com/login/oauth/access_token", json=auth_data, headers=headers)
        access_token = oauth_access_token.json()["access_token"]
        return await get_repositories(token=access_token)

@app.get("/")
async def index():
    session_state.SESSION_SECRET = RandomStringGenerator().generate_random_string(45)
    scope = "public_repo"
    state=session_state.SESSION_SECRET
    github_oauth_url = f"https://github.com/login/oauth/authorize?client_id={client_id}&X-OAuth-Scopes={scope}&X-Accepted-OAuth-Scopes={scope}&state={state}"
    return RedirectResponse(url=github_oauth_url)

async def get_repositories(token:str):
    async with httpx.AsyncClient() as client:
        headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + token,
        "X-GitHub-Api-Version": "2022-11-28"
        }
        starred_repositories = await client.get(f"https://api.github.com/user/starred", headers=headers)
        return starred_repositories.json()

if __name__ == "__main__":
    if not ConfigValidator().validate_secrets():
        print("Invalid configuration. Follow instructions in README to configure the application")
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)