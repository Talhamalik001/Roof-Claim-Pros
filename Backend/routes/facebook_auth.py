from fastapi import APIRouter, Request
from requests_oauthlib import OAuth2Session
from fastapi.responses import RedirectResponse

router = APIRouter()

# Facebook OAuth client config
FACEBOOK_CLIENT_ID = "731650043218243"
FACEBOOK_CLIENT_SECRET = "a102f591b1db8a485dda3d667c0d677a"
REDIRECT_URI = "http://localhost:9000/facebook/callback"

FACEBOOK_AUTH_URL = "https://www.facebook.com/v12.0/dialog/oauth"
FACEBOOK_TOKEN_URL = "https://graph.facebook.com/v12.0/oauth/access_token"
FACEBOOK_SCOPE = ['email', 'public_profile']

# ---------------- LOGIN ----------------
@router.get("/login")
async def facebook_login(request: Request):
    facebook = OAuth2Session(FACEBOOK_CLIENT_ID, redirect_uri=REDIRECT_URI, scope=FACEBOOK_SCOPE)
    authorization_url, _ = facebook.authorization_url(FACEBOOK_AUTH_URL)
    return RedirectResponse(authorization_url)

# ---------------- CALLBACK ----------------
@router.get("/callback")
async def facebook_callback(request: Request, code: str):
    # Create a new OAuth session and fetch the token using the provided code
    facebook = OAuth2Session(FACEBOOK_CLIENT_ID, redirect_uri=REDIRECT_URI)
    token = facebook.fetch_token(FACEBOOK_TOKEN_URL, client_secret=FACEBOOK_CLIENT_SECRET, code=code)
    
    # Retrieve the user's info from Facebook
    user_info = facebook.get('https://graph.facebook.com/me?fields=id,name,email').json()
    
    # Extract name and email from the user info
    name = user_info.get("name")
    email = user_info.get("email")
    
    # Log user info to check if email is missing
    print(f"User info from Facebook: {user_info}")
    
    if not email:
        email = "No email available"

    # Redirect to the notification page with user info
    return RedirectResponse(
        f"http://localhost:3000/notification?name={name}&email={email}"
    )