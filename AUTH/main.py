from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import os

import model as models
import schemas
import utils
from auth_database import getDB

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

app = FastAPI()

@app.get("/") # / means Home endpoint
def read_root():
    return {"Message":"This is the main app"}

@app.get("/greet")
def greet():
    return {"Greet":"hello World"}

# Create JWT Token
print(
    ACCESS_TOKEN_EXPIRE_MINUTES,
    type(ACCESS_TOKEN_EXPIRE_MINUTES)
)
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# Register User
@app.post("/signup")
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(getDB)
):
    existing_user = (
        db.query(models.User)
        .filter(models.User.username == user.username)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = utils.hash_password(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "role": new_user.role
    }


# Login
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(getDB)
):
    user = (
        db.query(models.User)
        .filter(models.User.username == form_data.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username"
        )

    if not utils.verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )

    token_data = {
        "sub": user.username,
        "role": user.role
    }

    access_token = create_access_token(token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# OAuth2 Scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Get Current User
def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")
        role = payload.get("role")

        if username is None or role is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    return {
        "username": username,
        "role": role
    }


# Protected Route
@app.get("/protected")
def protected_route(
    current_user: dict = Depends(get_current_user)
):
    return {
        "message": (
            f"Hello, {current_user['username']} | "
            f"You accessed a protected route"
        )
    }


# Role-Based Access Control
def require_roles(allowed_roles: list):
    def role_checker(
        current_user: dict = Depends(get_current_user)
    ):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        return current_user

    return role_checker


# User + Admin
@app.get("/profile")
def profile(
    current_user: dict = Depends(
        require_roles(["user", "admin"])
    )
):
    return {
        "message": (
            f"Profile of {current_user['username']} "
            f"({current_user['role']})"
        )
    }


# User Only
@app.get("/user/dashboard")
def user_dashboard(
    current_user: dict = Depends(
        require_roles(["user"])
    )
):
    return {
        "message": "Welcome User"
    }


# Admin Only
@app.get("/admin/dashboard")
def admin_dashboard(
    current_user: dict = Depends(
        require_roles(["admin"])
    )
):
    return {
        "message": "Welcome Admin"
    }