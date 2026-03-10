from pydantic import BaseModel

# OTP related schemas
class EmailRequest(BaseModel):
    email: str

class VerifyRequest(BaseModel):
    email: str
    otp: str

# User registration/login schemas
class RegisterRequest(BaseModel):
    email: str
    firstName: str
    lastName: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str