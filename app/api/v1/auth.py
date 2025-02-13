from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated
from app.schemas.item_schemas import UserCreate, UserResponse
from app.database.connection import get_db
from app.database.models import User
from sqlalchemy.orm import Session
from app.utils.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
)

router = APIRouter(prefix="/auth", tags=["auth"])

# OAuth2 Configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Endpoint for user registration
@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    - **Parameters**:
        - `user`: UserCreate schema containing user details (name, email, password).
        - `db`: Database session dependency.

    - **Returns**:
        - UserResponse schema with the newly created user's details.

    - **Raises**:
        - HTTPException (400): If the email is already registered.
    """
    # Check if the user already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create a new user
    hashed_password =  get_password_hash(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Endpoint for user login
@router.post("/token")
def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db),
):
    """
    Authenticate a user and generate a JWT token.

    - **Parameters**:
        - `form_data`: OAuth2PasswordRequestForm containing username (email) and password.
        - `db`: Database session dependency.

    - **Returns**:
        - A dictionary containing the JWT token and its type.

    - **Raises**:
        - HTTPException (401): If the email or password is incorrect.
    """
    # Authenticate the user
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create the JWT token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint to get current user information
@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Retrieve information about the authenticated user.

    - **Parameters**:
        - `current_user`: The authenticated user (retrieved via JWT token).

    - **Returns**:
        - UserResponse schema with the authenticated user's details.
    """
    return current_user
