from pydantic import BaseModel, EmailStr

class Register(BaseModel):
    email: EmailStr
    hashed_pwd: str
    role: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"