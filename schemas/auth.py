from pydantic import BaseModel, EmailStr

class Register(BaseModel):
    email: EmailStr
    name: str
    password: str
    role: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    
    class Config:
        from_attributes = True