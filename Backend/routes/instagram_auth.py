from fastapi import APIRouter, Request
from requests_oauthlib import OAuth2Session
from fastapi.responses import RedirectResponse
import requests

router = APIRouter()

from config import INSTAGRAM_CLIENT_ID, INSTAGRAM_CLIENT_SECRET

# Instagram OAuth client config
REDIRECT_URI = "http://localhost:9000/instagram/callback"  # Redirect URI for callback

INSTAGRAM_AUTH_URL = "https://api.instagram.com/oauth/authorize"
INSTAGRAM_TOKEN_URL = "https://api.instagram.com/oauth/access_token"
INSTAGRAM_SCOPE = ['user_profile']

# ---------------- LOGIN ----------------
@router.get("/login")
async def instagram_login(request: Request):
    instagram = OAuth2Session(INSTAGRAM_CLIENT_ID, redirect_uri=REDIRECT_URI, scope=INSTAGRAM_SCOPE)
    authorization_url, _ = instagram.authorization_url(INSTAGRAM_AUTH_URL)
    return RedirectResponse(authorization_url)

# ---------------- CALLBACK ----------------
@router.get("/callback")
async def instagram_callback(request: Request, code: str):
    # Step 1: Exchange code for access token
    token_url = INSTAGRAM_TOKEN_URL
    data = {
        "client_id": INSTAGRAM_CLIENT_ID,
        "client_secret": INSTAGRAM_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": code
    }
    token_response = requests.post(token_url, data=data)

    if token_response.status_code != 200:
        return HTMLResponse(f"<h1>Error fetching access token</h1><p>{token_response.text}</p>")

    access_token = token_response.json().get("access_token")
    if not access_token:
        return HTMLResponse("<h1>Failed to get access token</h1>")

    # Step 2: Fetch user info using access token
    user_info_url = f"https://graph.instagram.com/me?fields=id,username&access_token={access_token}"
    user_response = requests.get(user_info_url)

    if user_response.status_code != 200:
        return HTMLResponse(f"<h1>Error fetching user info</h1><p>{user_response.text}</p>")

    user = user_response.json()

    # Step 3: Redirect to the notification page with user info
    return RedirectResponse(
        f"http://localhost:3000/notification?username={user['username']}&user_id={user['id']}"
    )