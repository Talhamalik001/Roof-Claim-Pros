from fastapi import APIRouter, HTTPException
from schemas.schemas import EmailRequest, VerifyRequest, RegisterRequest, LoginRequest
from services.otp_service import generate_otp, verify_otp

from fastapi import APIRouter, HTTPException
from fastapi import APIRouter, HTTPException, Request

router = APIRouter()

# Temporary in-memory user store
users_db = {}  # {"email": {"firstName":..., "lastName":..., "password":...}}

# ---------------- OTP ROUTES ----------------
@router.post("/send-otp")
async def send_otp(data: EmailRequest):
    await generate_otp(data.email)
    return {"message": "OTP sent to your email!"}

@router.post("/verify-otp")
def verify(data: VerifyRequest):
    if verify_otp(data.email, data.otp):
        return {"status": "success"}
    return {"status": "failed"}

# ---------------- USER AUTH ROUTES ----------------
@router.post("/register")
def register_user(data: RegisterRequest):
    if data.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[data.email] = {
        "firstName": data.firstName,
        "lastName": data.lastName,
        "email": data.email,
        "password": data.password
    }
    return {"status": "success"}

# @router.post("/login")
# def login_user(data: LoginRequest):
#     user = users_db.get(data.email)
#     if not user or user["password"] != data.password:
#         raise HTTPException(status_code=401, detail="Invalid email or password")
#     return {"status": "success", "firstName": user["firstName"]}
@router.post("/login")
def login_user(data: LoginRequest, request: Request):

    user = users_db.get(data.email)

    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # session create
    request.session["user"] = data.email

    return {
        "status": "success",
        "firstName": user["firstName"]
    }



@router.post("/logout")
def logout_user(request: Request):

    request.session.clear()

    return {"message": "Logged out successfully"}












#12345678QWERqwe!@#$