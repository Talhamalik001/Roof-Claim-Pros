from fastapi import APIRouter, Request
from requests_oauthlib import OAuth2Session
from fastapi.responses import RedirectResponse

from dotenv import load_dotenv
import os

load_dotenv()

FACEBOOK_CLIENT_ID = os.getenv("FACEBOOK_CLIENT_ID")
FACEBOOK_CLIENT_SECRET = os.getenv("FACEBOOK_CLIENT_SECRET")

FACEBOOK_REDIRECT_URI = os.getenv("FACEBOOK_REDIRECT_URI")

FACEBOOK_AUTH_URL = os.getenv("FACEBOOK_AUTH_URL")
FACEBOOK_TOKEN_URL = os.getenv("FACEBOOK_TOKEN_URL")
FACEBOOK_USER_INFO_URL = os.getenv("FACEBOOK_USER_INFO_URL")

FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL")
router = APIRouter()

from config import (
    FACEBOOK_CLIENT_ID,
    FACEBOOK_CLIENT_SECRET,
    FACEBOOK_REDIRECT_URI,
    FACEBOOK_AUTH_URL,
    FACEBOOK_TOKEN_URL,
    FACEBOOK_USER_INFO_URL,
    FRONTEND_BASE_URL
)

FACEBOOK_SCOPE = ['email', 'public_profile']


# ---------------- LOGIN ----------------
@router.get("/login")
async def facebook_login(request: Request):

    facebook = OAuth2Session(
        FACEBOOK_CLIENT_ID,
        redirect_uri=FACEBOOK_REDIRECT_URI,
        scope=FACEBOOK_SCOPE
    )

    authorization_url, _ = facebook.authorization_url(FACEBOOK_AUTH_URL)

    return RedirectResponse(authorization_url)


# ---------------- CALLBACK ----------------
@router.get("/callback")
async def facebook_callback(request: Request, code: str):

    facebook = OAuth2Session(
        FACEBOOK_CLIENT_ID,
        redirect_uri=FACEBOOK_REDIRECT_URI
    )

    token = facebook.fetch_token(
        FACEBOOK_TOKEN_URL,
        client_secret=FACEBOOK_CLIENT_SECRET,
        code=code
    )

    # Get user info
    user_info = facebook.get(FACEBOOK_USER_INFO_URL).json()

    name = user_info.get("name")
    email = user_info.get("email")

    print(f"User info from Facebook: {user_info}")

    if not email:
        email = "No email available"

    return RedirectResponse(
        f"{FRONTEND_BASE_URL}/notification?name={name}&email={email}"
    )