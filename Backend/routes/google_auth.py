import base64
import hashlib
import secrets
import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
from starlette.requests import Request
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# ENV VARIABLES
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
GOOGLE_AUTH_URI = os.getenv("GOOGLE_AUTH_URI")
GOOGLE_TOKEN_URI = os.getenv("GOOGLE_TOKEN_URI")

GOOGLE_SCOPE_OPENID = os.getenv("GOOGLE_SCOPE_OPENID")
GOOGLE_SCOPE_EMAIL = os.getenv("GOOGLE_SCOPE_EMAIL")
GOOGLE_SCOPE_PROFILE = os.getenv("GOOGLE_SCOPE_PROFILE")

FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL")


CLIENT_CONFIG = {
    "web": {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "auth_uri": GOOGLE_AUTH_URI,
        "token_uri": GOOGLE_TOKEN_URI,
    }
}

SCOPES = [
    GOOGLE_SCOPE_OPENID,
    GOOGLE_SCOPE_EMAIL,
    GOOGLE_SCOPE_PROFILE,
]


def generate_code_verifier():
    return secrets.token_urlsafe(64)


def generate_code_challenge(code_verifier):
    return base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode("utf-8")).digest()
    ).decode("utf-8").rstrip("=")


# ---------------- LOGIN ----------------
@router.get("/login")
async def login(request: Request):

    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)

    request.session["code_verifier"] = code_verifier

    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI,
    )

    auth_url, _ = flow.authorization_url(
        access_type="offline",
        prompt="consent",
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )

    return RedirectResponse(auth_url)


# ---------------- CALLBACK ----------------
@router.get("/callback")
async def callback(request: Request, code: str):

    code_verifier = request.session.get("code_verifier")

    if not code_verifier:
        raise HTTPException(status_code=400, detail="Missing code verifier")

    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI,
    )

    flow.fetch_token(code=code, code_verifier=code_verifier)

    credentials = flow.credentials

    id_info = id_token.verify_oauth2_token(
        credentials.id_token,
        requests.Request(),
        GOOGLE_CLIENT_ID
    )

    name = id_info.get("name")
    email = id_info.get("email")

    return RedirectResponse(
        f"{FRONTEND_BASE_URL}/notification?name={name}&email={email}"
    )