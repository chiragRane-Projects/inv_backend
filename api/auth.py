from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User
from schemas.auth import LoginRequest, TokenResponse, Register
from core.security import verify_pwd, create_access_token, hash_pwd

router = APIRouter(prefix="/auth", tags=['Auth'])

@router.post('/register')
def register(data:Register, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    
    if user: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with this email already exists'
        )
    
    hashed = hash_pwd(data.hashed_pwd)
    
    new_user = User(
        email = data.email,
        hashed_pwd = hashed,
        role = data.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }
    
@router.post('/login', response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid credentials'
        )
        
    if not verify_pwd(data.password, user.hashed_pwd):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid credentials'
        )
        
    token = create_access_token({
        "user_id": user.id, "role": user.role
    })
    
    print(user.email ,user.role)
    return {"access_token": token}