

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


load_dotenv()

app = FastAPI()

origins = os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")
methods = os.getenv("CORS_ALLOW_METHODS", "*").split(",")
headers = os.getenv("CORS_ALLOW_HEADERS", "*").split(",")
credentials = os.getenv("CORS_ALLOW_CREDENTIALS", "True") == "True"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=methods,
    allow_headers=headers,
    allow_credentials=credentials,
)

# ---------------- CORS ----------------


secret_key = secrets.token_hex(32)  # Secure, random key
app.add_middleware(SessionMiddleware, secret_key=secret_key ,  max_age=60)

# ---------------- Include Routers ----------------
app.include_router(auth_router, prefix="/auth")
app.include_router(google_router, prefix="/google")
app.include_router(facebook_router, prefix="/facebook")  # Register Facebook router
app.include_router(instagram_router, prefix="/instagram")







# In-memory storage
leads: List[Lead] = []

@app.post("/leads")
async def add_lead(lead: Lead):
    leads.append(lead)
    return {"message": "Lead added successfully"}

@app.get("/leads", response_model=List[Lead])
async def get_leads():
    return leads


@app.put("/leads/{lead_index}")
async def update_lead(lead_index: int, lead: Lead):
    try:
        leads[lead_index] = lead
        return {"message": "Lead updated", "lead": lead}
    except IndexError:
        raise HTTPException(status_code=404, detail="Lead not found")

@app.delete("/leads/{lead_index}")
async def delete_lead(lead_index: int):
    try:
        deleted = leads.pop(lead_index)
        return {"message": "Lead deleted", "lead": deleted}
    except IndexError:
        raise HTTPException(status_code=404, detail="Lead not found")
