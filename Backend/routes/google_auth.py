# from fastapi import FastAPI, Request
# from fastapi.responses import RedirectResponse
# from fastapi.templating import Jinja2Templates
# from google_auth_oauthlib.flow import Flow
# from google.oauth2 import id_token
# from google.auth.transport import requests
# import os

# app = FastAPI()
# templates = Jinja2Templates(directory="templates")
# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# GOOGLE_CLIENT_ID = "314093001784-vc7qmmbosom6al9n1mo55blghd5tlscm.apps.googleusercontent.com"
# GOOGLE_CLIENT_SECRET = "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"

# CLIENT_CONFIG = {
#     "web": {
#         "client_id": GOOGLE_CLIENT_ID,
#         "client_secret": GOOGLE_CLIENT_SECRET,
#         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#         "token_uri": "https://oauth2.googleapis.com/token",
#     }
# }

# # Simple in-memory storage for demo (state verification)
# state_storage = {}

# @app.get("/")
# async def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# @app.get("/login")
# async def login():
#     flow = Flow.from_client_config(
#         CLIENT_CONFIG,
#         scopes=["openid", "email", "profile"],
#         redirect_uri="http://localhost:8000/callback"
#     )
#     auth_url, state = flow.authorization_url()
#     state_storage[state] = flow  # store flow object for this state
#     return RedirectResponse(auth_url)

# @app.get("/callback")
# async def callback(request: Request):
#     try:
#         state = request.query_params.get("state")
#         if not state or state not in state_storage:
#             return {"error": "Invalid state"}

#         flow = state_storage.pop(state)  # get the flow for this login

#         # Fetch token using Google response
#         flow.fetch_token(authorization_response=str(request.url))
#         id_info = id_token.verify_oauth2_token(
#             flow.credentials.id_token,
#             requests.Request(),
#             GOOGLE_CLIENT_ID
#         )

#         return templates.TemplateResponse(
#             "profile.html",
#             {"request": request, "name": id_info.get("name"), "email": id_info.get("email")}
#         )

#     except Exception as e:
#         return {"error": str(e)}

# import os
# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# from fastapi import APIRouter, Request
# from fastapi.responses import RedirectResponse  # For redirecting after login
# from google_auth_oauthlib.flow import Flow
# from google.oauth2 import id_token
# from google.auth.transport import requests
# import os

# router = APIRouter()

# # ------------------------ Google OAuth Config ------------------------
# GOOGLE_CLIENT_ID = "314093001784-vc7qmmbosom6al9n1mo55blghd5tlscm.apps.googleusercontent.com"
# GOOGLE_CLIENT_SECRET = "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"
# CLIENT_CONFIG = {
#     "web": {
#         "client_id": GOOGLE_CLIENT_ID,
#         "client_secret": GOOGLE_CLIENT_SECRET,
#         "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#         "token_uri": "https://oauth2.googleapis.com/token",
#     }
# }

# SCOPES = [
#     "openid",
#     "https://www.googleapis.com/auth/userinfo.email",
#     "https://www.googleapis.com/auth/userinfo.profile",
# ]

# REDIRECT_URI = "http://localhost:9000/google/callback"
# # ------------------------ Routes ------------------------

# @router.get("/login")
# async def login(request: Request):

#     flow = Flow.from_client_config(
#         CLIENT_CONFIG,
#         scopes=SCOPES,
#         redirect_uri=REDIRECT_URI
#     )

#     auth_url, state = flow.authorization_url(
#         access_type="offline",
#         prompt="consent"
#     )

#     request.session["state"] = state

#     return RedirectResponse(auth_url)



# @router.get("/callback")
# async def callback(request: Request):

#     state = request.session.get("state")

#     flow = Flow.from_client_config(
#         CLIENT_CONFIG,
#         scopes=SCOPES,
#         state=state,
#         redirect_uri=REDIRECT_URI
#     )

#     flow.fetch_token(authorization_response=str(request.url))

#     credentials = flow.credentials

#     id_info = id_token.verify_oauth2_token(
#         credentials.id_token,
#         requests.Request(),
#         GOOGLE_CLIENT_ID
#     )

#     name = id_info.get("name")
#     email = id_info.get("email")

#     return RedirectResponse(
#         f"http://localhost:3000/notification?name={name}&email={email}"
#     )

# # except Exception as e:
# #     return {"error": str(e)}



# # @router.get("/callback")
# # async def callback(request: Request):
# #     try:
# #         # Recreate Flow (fresh object)
# #         flow = Flow.from_client_config(
# #             CLIENT_CONFIG,
# #             scopes=SCOPES,
# #             redirect_uri=REDIRECT_URI
# #         )

# #         # Fetch token using the callback URL
# #         flow.fetch_token(authorization_response=str(request.url))

# #         # Verify Google ID token
# #         id_info = id_token.verify_oauth2_token(
# #             flow.credentials.id_token,
# #             requests.Request(),
# #             GOOGLE_CLIENT_ID
# #         )

# #         # Redirect to the notification page with user data (you can pass query params)
# #         return RedirectResponse(url="http://localhost:3000/notification?name=" + id_info.get("name") + "&email=" + id_info.get("email"))

# #     except Exception as e:
# #         return {"error": str(e)}
 
import base64
import hashlib
import secrets
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware

router = APIRouter()

from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

# Google OAuth client config
REDIRECT_URI = "http://localhost:9000/google/callback"

CLIENT_CONFIG = {
    "web": {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
}

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

# Generate Code Verifier and Code Challenge (PKCE)
def generate_code_verifier():
    return secrets.token_urlsafe(64)

def generate_code_challenge(code_verifier):
    # Create SHA256 hash of the code verifier
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8').rstrip("=")
    return code_challenge

# ---------------- LOGIN ----------------
@router.get("/login")
async def login(request: Request):
    # Generate the code verifier and code challenge
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)

    # Store the code_verifier in the session
    request.session['code_verifier'] = code_verifier  # Store securely in the session

    # Create the OAuth Flow instance
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )

    # Generate the authorization URL with PKCE
    auth_url, _ = flow.authorization_url(
        access_type="offline",
        prompt="consent",
        code_challenge=code_challenge,
        code_challenge_method="S256",  # This is the recommended method for PKCE
    )

    return RedirectResponse(auth_url)

# ---------------- CALLBACK ----------------
@router.get("/callback")
async def callback(request: Request, code: str):
    # Retrieve the code_verifier from the session
    code_verifier = request.session.get('code_verifier')
    
    if not code_verifier:
        raise HTTPException(status_code=400, detail="Missing code verifier")

    # Create the OAuth Flow instance
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )

    # Fetch the token using the provided code and the stored code_verifier
    flow.fetch_token(code=code, code_verifier=code_verifier)

    credentials = flow.credentials

    # Verify the ID token
    id_info = id_token.verify_oauth2_token(
        credentials.id_token,
        requests.Request(),
        GOOGLE_CLIENT_ID
    )

    name = id_info.get("name")
    email = id_info.get("email")

    # Redirect to the notification page with the user's name and email
    return RedirectResponse(
        f"http://localhost:3000/notification?name={name}&email={email}"
    )