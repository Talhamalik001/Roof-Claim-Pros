# from fastapi import FastAPI
# from routes.auth_routes import router  # import router from routes
# from routes import google_auth

# from fastapi.middleware.cors import CORSMiddleware



# app = FastAPI()  # create FastAPI app instance
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # ya ["http://localhost:3000"]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# app.include_router(router)  # include auth routes
# from routes import google_auth

# app.include_router(google_auth.router)
 

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.sessions import SessionMiddleware  # Correct import
# from routes.auth_routes import router as auth_router
# from routes.google_auth import router as google_router  # Correct import

# app = FastAPI(title="RoofClaimPros Backend")

# # ---------------- CORS ----------------
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # React dev server / other frontend origin
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ---------------- Session Middleware ----------------
# app.add_middleware(SessionMiddleware, secret_key="your-secret-key")  # Add this line to enable session handling

# # ---------------- Include Routers ----------------
# app.include_router(auth_router, prefix="/auth")  # Routes like /auth/register, /auth/login, etc.
# app.include_router(google_router, prefix="/google")  # Routes like /google/login, /google/callback

# # ---------------- Root Test ----------------
# @app.get("/")
# async def root():
#     return {"message": "RoofClaimPros Backend is running 🚀"}

# import secrets
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.sessions import SessionMiddleware
# from routes.auth_routes import router as auth_router
# from routes.google_auth import router as google_router


# from routes.facebook_auth import router as facebook_router  # Make sure this import is correct



# app = FastAPI(title="RoofClaimPros Backend")

# # ---------------- CORS ----------------
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins for now
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# secret_key = secrets.token_hex(32)  # Secure, random key
# app.add_middleware(SessionMiddleware, secret_key=secret_key)
# # ---------------- Session Middleware ----------------
#  # Add this line to enable session handling

# # ---------------- Include Routers ----------------
# app.include_router(auth_router, prefix="/auth")  # Routes like /auth/register, /auth/login, etc.
# app.include_router(google_router, prefix="/google")  # Routes like /google/login, /google/callback
# app.include_router(facebook_router, prefix="/facebook")  # Ensure this line is included

# # ---------------- Root Test ----------------
# @app.get("/")
# async def root():
#     return {"message": "RoofClaimPros Backend is running"}

from pydantic import BaseModel
from typing import List


import secrets
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from routes.auth_routes import router as auth_router
from routes.google_auth import router as google_router
from routes.facebook_auth import router as facebook_router  # Import Facebook router
from routes.instagram_auth import router as instagram_router
app = FastAPI(title="RoofClaimPros Backend")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

secret_key = secrets.token_hex(32)  # Secure, random key
app.add_middleware(SessionMiddleware, secret_key=secret_key ,  max_age=60)

# ---------------- Include Routers ----------------
app.include_router(auth_router, prefix="/auth")
app.include_router(google_router, prefix="/google")
app.include_router(facebook_router, prefix="/facebook")  # Register Facebook router
app.include_router(instagram_router, prefix="/instagram")
# ---------------- Root Test ----------------
@app.get("/")
async def root():
    return {"message": "RoofClaimPros Backend is running"}



# Lead schema
class Lead(BaseModel):
    name: str
    contactInfo: str
    propertyAddress: str
    status: str

# In-memory storage
leads: List[Lead] = []

@app.post("/leads")
async def add_lead(lead: Lead):
    leads.append(lead)
    return {"message": "Lead added successfully"}

@app.get("/leads", response_model=List[Lead])
async def get_leads():
    return leads


@app.delete("/leads/{lead_index}")
async def delete_lead(lead_index: int):
    if 0 <= lead_index < len(leads):
        deleted = leads.pop(lead_index)
        return {"message": "Lead deleted", "lead": deleted}
    return {"error": "Lead not found"}