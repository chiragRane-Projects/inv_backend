from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from core.security import SECRET_KEY, ALGORITHM
from models.user import User
from core.database import get_db
from sqlalchemy.orm import Session
from typing import Set


def get_current_user(db: Session = Depends(get_db), token: str = Depends):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
        
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return user

def require_role(*allowed_roles: str):
    allowed_roles_set: Set[str] = set(allowed_roles)
    def role_checker(user: User = Depends(get_current_user)):
        if user.role not in allowed_roles_set:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permission"
            )
        return user
    return role_checker
