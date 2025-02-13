from app.utils.auth import verify_password, get_password_hash, create_access_token
from datetime import timedelta

def test_verify_password():
    """
    Test the `verify_password` function.

    - **Steps**:
        1. Generates a hash for a plain password.
        2. Verifies if the plain password matches the hash.
        3. Verifies if an incorrect password does not match the hash.

    - **Assertions**:
        - The correct password should return `True`.
        - An incorrect password should return `False`.
    """
    # Original password
    plain_password = "password123"

    # Generates the password hash
    hashed_password = get_password_hash(plain_password)

    # Checks if the password is valid
    assert verify_password(plain_password, hashed_password) == True
    assert verify_password("wrong password", hashed_password) == False

def test_create_access_token():
    """
    Test the `create_access_token` function.

    - **Steps**:
        1. Creates a JWT token with a payload containing a user email.
        2. Verifies if the token is successfully created.

    - **Assertions**:
        - The token should not be `None`.
    """
    # Data for the token
    data = {"sub": "user@example.com"}

    # Create token with expiration time
    token = create_access_token(data, expires_delta=timedelta(minutes=30))

    # Checks if the token was created
    assert token is not None
