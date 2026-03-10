from pydantic import BaseModel

class EmailRequest(BaseModel):
    email: str

class VerifyRequest(BaseModel):
    email: str
    otp: str

    #formic ,  yup (validation)