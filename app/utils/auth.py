from datetime import datetime, timedelta, UTC
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import User
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Security Settings
SECRET_KEY = os.getenv("SECRET_KEY") # Secret key for JWT encoding/decoding
ALGORITHM = os.getenv("ALGORITHM") # Algorithm used for JWT encoding/decoding
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") # Token expiration time

# Setting the encryption context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 Configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Function to check password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if a plain password matches a hashed password.

    - **Parameters**:
        - `plain_password`: The plain text password to verify.
        - `hashed_password`: The hashed password to compare against.

    - **Returns**:
        - `True` if the passwords match, otherwise `False`.
    """
    return pwd_context.verify(plain_password, hashed_password)

# Function to generate the password hash
def get_password_hash(password: str) -> str:
    """
    Generates a hash for a given password.

    - **Parameters**:
        - `password`: The plain text password to hash.

    - **Returns**:
        - The hashed password.
    """
    return pwd_context.hash(password)

# Function to authenticate the user
def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Authenticates a user by checking their email and password.

    - **Parameters**:
        - `db`: Database session.
        - `email`: The email of the user to authenticate.
        - `password`: The password of the user to authenticate.

    - **Returns**:
        - The authenticated user if successful, otherwise `None`.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return None
    return user

# Function to create the JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT token with the provided data and expiration time.

    - **Parameters**:
        - `data`: A dictionary containing the data to encode in the token (e.g., user email).
        - `expires_delta`: Optional timedelta for token expiration. Defaults to 15 minutes.

    - **Returns**:
        - The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to get the current user
def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Retrieves the current authenticated user from the JWT token.

    - **Parameters**:
        - `db`: Database session.
        - `token`: The JWT token provided in the request header.

    - **Returns**:
        - The authenticated user.

    - **Raises**:
        - HTTPException (401): If the token is invalid or the user is not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
