from jose import JWTError, jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.app.database.db import get_db, User

# Secret keys for JWT
SECRET_KEY = "HEARTCARE_AI_SUPER_SECRET_KEY_FOR_JWT_SECURITY_DO_NOT_SHARE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 240  # 4 hours session duration

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.email == username).first()
    if user is None:
        from database.db import Patient
        patient = db.query(Patient).filter(Patient.id == username).first()
        if patient:
            user = User(id=-1, name=patient.name, email=patient.id, role="patient")
        else:
            raise credentials_exception
    return user

def check_role(roles: list[str]):
    def dependency(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Action forbidden for role: {current_user.role}. Requires one of: {roles}"
            )
        return current_user
    return dependency

# Common role checks
def get_current_doctor_or_admin(current_user: User = Depends(check_role(["doctor", "admin"]))):
    return current_user

def get_current_admin(current_user: User = Depends(check_role(["admin"]))):
    return current_user

def get_current_doctor(current_user: User = Depends(check_role(["doctor"]))):
    return current_user
