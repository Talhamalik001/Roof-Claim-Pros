from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from requests_oauthlib import OAuth2Session
import requests
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

INSTAGRAM_CLIENT_ID = os.getenv("INSTAGRAM_CLIENT_ID")
INSTAGRAM_CLIENT_SECRET = os.getenv("INSTAGRAM_CLIENT_SECRET")
INSTAGRAM_REDIRECT_URI = os.getenv("INSTAGRAM_REDIRECT_URI")

INSTAGRAM_AUTH_URL = os.getenv("INSTAGRAM_AUTH_URL")
INSTAGRAM_TOKEN_URL = os.getenv("INSTAGRAM_TOKEN_URL")
INSTAGRAM_GRAPH_URL = os.getenv("INSTAGRAM_GRAPH_URL")

INSTAGRAM_SCOPE = os.getenv("INSTAGRAM_SCOPE").split(",")

FRONTEND_URL = os.getenv("FRONTEND_URL")


# -------- LOGIN --------
@router.get("/login")
async def instagram_login():

    instagram = OAuth2Session(
        INSTAGRAM_CLIENT_ID,
        redirect_uri=INSTAGRAM_REDIRECT_URI,
        scope=INSTAGRAM_SCOPE
    )

    authorization_url, _ = instagram.authorization_url(INSTAGRAM_AUTH_URL)

    return RedirectResponse(authorization_url)


# -------- CALLBACK --------
@router.get("/callback")
async def instagram_callback(code: str):

    data = {
        "client_id": INSTAGRAM_CLIENT_ID,
        "client_secret": INSTAGRAM_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": INSTAGRAM_REDIRECT_URI,
        "code": code
    }

    token_response = requests.post(INSTAGRAM_TOKEN_URL, data=data)

    if token_response.status_code != 200:
        return HTMLResponse("Error fetching access token")

    access_token = token_response.json().get("access_token")

    if not access_token:
        return HTMLResponse("Failed to get access token")

    user_url = f"{INSTAGRAM_GRAPH_URL}?fields=id,username&access_token={access_token}"
    user = requests.get(user_url).json()

    return RedirectResponse(
        f"{FRONTEND_URL}/notification?username={user['username']}&user_id={user['id']}"
    )