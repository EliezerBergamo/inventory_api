import pytest
import uuid
from fastapi.testclient import TestClient
from main import app
from app.database.connection import SessionLocal, engine
from app.utils.auth import create_access_token
from app.database.models import Base, User, Category

# Fixture to create database session
@pytest.fixture
def db_session():
    """
    Fixture to create a database session for testing.

    - **Yields**:
        - A database session for use in tests.

    - **Cleans up**:
        - Drops all tables after the test to ensure a clean state.
    """
    # Creates a new database session
    db = SessionLocal()
    try:
        # Creates the tables in the database to ensure they exist
        Base.metadata.create_all(bind=db.bind)
        yield db  # Session will be provided for testing
    finally:
        db.close()  # Close the session after the test
        # Optional: Cleans up tables after testing to ensure the database is clean
        Base.metadata.drop_all(bind=db.bind)

# Test client creation
@pytest.fixture(scope="module")
def client():
    """
    Fixture to create a test client for the FastAPI application.

    - **Yields**:
        - A TestClient instance for making HTTP requests.

    - **Cleans up**:
        - Drops all tables after the test to ensure a clean state.
    """
    # Create tables in the database for testing
    Base.metadata.create_all(bind=engine)

    # Instantiate the test client
    with TestClient(app) as client:
        yield client

    # Cleaning the database after testing
    Base.metadata.drop_all(bind=engine)

# Fixture to create a test user
@pytest.fixture
def create_test_user(db_session):
    """
    Fixture to create a test user in the database.

    - **Parameters**:
        - `db_session`: Database session.

    - **Returns**:
        - A tuple containing a mocked access token and the created user.
    """
    user = User(name="Test User", email="testuser@example.com", password="password")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    access_token = "mocked_token"  # # A valid token must be generated here using the authentication method
    return access_token, user

# Fixture to create a category in the database
@pytest.fixture
def create_category(db_session):
    """
    Fixture to create a test category in the database.

    - **Parameters**:
        - `db_session`: Database session.

    - **Returns**:
        - The created category.
    """
    category = Category(id=uuid.uuid4(), name="Test Category", description="A test category")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category

def test_create_product(client, create_test_user, create_category):
    """
   Test the creation of a product.

   - **Steps**:
       1. Creates a test user and generates an access token.
       2. Creates a test category.
       3. Sends a POST request to create a new product.
       4. Verifies if the response status is 200 (OK).
   """
    # The first item in the tuple is the token, the second is the user
    access_token, test_user = create_test_user  # Accessing the user

    # It is now possible to access the user's email.
    access_token = create_access_token(data={"sub": test_user.email})  # Using the user's email

    # Debug: Check token value
    print(f"Access Token: {access_token}")

    # Use the category directly
    category = create_category

    # Data for the new product
    product_data = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 100.0,
        "stock_quantity": 50,
        "image_url": "http://example.com/product.jpg",
        "category_id": str(category.id),  # Using the created category ID
        "user_id": str(test_user.id)  # Adding the user ID
    }

    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.post("/api/v1/products/", json=product_data, headers=headers)

    # Debug: Print detailed response
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.content}")

    # Check the JSON response for more details about the error
    if response.status_code == 422:
        print("Detailed error:", response.json())

    assert response.status_code == 200

def test_list_products(client, create_test_user, create_category):
    """
    Test the listing of products.

    - **Steps**:
        1. Creates a test user and generates an access token.
        2. Creates a test category and a product.
        3. Sends a GET request to list the products.
        4. Verifies if the response status is 200 (OK) and if the product is listed.
    """
    # Gets the token and test user
    access_token, test_user = create_test_user
    # Generates a valid access token
    access_token = create_access_token(data={"sub": test_user.email})

    product_data = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 100.0,
        "stock_quantity": 50,
        "image_url": "http://example.com/product.jpg",
        "category_id": str(create_category.id),
        "user_id": str(test_user.id)
    }

    headers = {"Authorization": f"Bearer {access_token}"}

    # Create a product
    client.post("/api/v1/products/", json=product_data, headers=headers)

    # Make a request to list the products
    response = client.get("/api/v1/products/", headers=headers)

    # Debug: Print detailed response
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.content}")

    # Checks if the status code is 200 and if the product is on the list
    assert response.status_code == 200
    assert len(response.json()) > 0  # Check that there is at least one product listed

    # Checks if the product description is correct
    assert response.json()[0]['description'] == product_data["description"]

def test_read_product(client, create_test_user, create_category):
    """
    Test reading a specific product.

    - **Steps**:
        1. Creates a test user and generates an access token.
        2. Creates a test category and a product.
        3. Sends a GET request to read the product.
        4. Verifies if the response status is 200 (OK) and if the product data is correct.
    """
    # Gets the token and test user
    access_token, test_user = create_test_user
    # Generates a valid access token
    access_token = create_access_token(data={"sub": test_user.email})

    product_data = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 100.0,
        "stock_quantity": 50,
        "image_url": "http://example.com/product.jpg",
        "category_id": str(create_category.id),
        "user_id": str(test_user.id)
    }

    headers = {"Authorization": f"Bearer {access_token}"}

    # Create the product
    response_create = client.post("/api/v1/products/", json=product_data, headers=headers)
    created_product = response_create.json()

    # Make a request to read the product
    response = client.get(f"/api/v1/products/{created_product['id']}", headers=headers)

    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.content}")

    # Check if the answer is 200 OK
    assert response.status_code == 200

    # Check that the returned product data is correct
    response_json = response.json()
    assert response_json["description"] == product_data["description"]
    assert response_json["price"] == product_data["price"]
    assert response_json["stock_quantity"] == product_data["stock_quantity"]
    assert response_json["image_url"] == product_data["image_url"]
    assert response_json["category_id"] == str(create_category.id)
    assert response_json["user_id"] == str(test_user.id)

def test_update_product(client, create_test_user, create_category):
    """
    Test updating a product.

    - **Steps**:
        1. Creates a test user and generates an access token.
        2. Creates a test category and a product.
        3. Sends a PUT request to update the product.
        4. Verifies if the response status is 200 (OK) and if the product data is updated.
    """
    # Gets the token and test user
    access_token, test_user = create_test_user
    # Generates a valid access token
    access_token = create_access_token(data={"sub": test_user.email})

    product_data = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 100.0,
        "stock_quantity": 50,
        "image_url": "http://example.com/product.jpg",
        "category_id": str(create_category.id),
        "user_id": str(test_user.id)
    }

    headers = {"Authorization": f"Bearer {access_token}"}

    # Create the product
    response_create = client.post("/api/v1/products/", json=product_data, headers=headers)
    created_product = response_create.json()

    # Updated product data
    updated_product_data = {
        "name": "Updated Product",
        "description": "This is an updated test product",
        "price": 150.0,
        "stock_quantity": 30,
        "image_url": "http://example.com/updated_product.jpg",
        "category_id": str(create_category.id),
        "user_id": str(test_user.id)
    }

    # Make a request to update the product
    response_update = client.put(f"/api/v1/products/{created_product['id']}", json=updated_product_data, headers=headers)

    print(f"Response status code: {response_update.status_code}")
    print(f"Response content: {response_update.content}")

    assert response_update.status_code == 200

    # Checks whether the returned product data is up to date
    response_json = response_update.json()
    assert response_json["description"] == updated_product_data["description"]
    assert response_json["price"] == updated_product_data["price"]
    assert response_json["stock_quantity"] == updated_product_data["stock_quantity"]
    assert response_json["image_url"] == updated_product_data["image_url"]
    assert response_json["category_id"] == str(create_category.id)
    assert response_json["user_id"] == str(test_user.id)

def test_delete_product(client, create_test_user, create_category):
    """
    Test deleting a product.

    - **Steps**:
        1. Creates a test user and generates an access token.
        2. Creates a test category and a product.
        3. Sends a DELETE request to delete the product.
        4. Verifies if the response status is 200 (OK) and if the product no longer exists.
    """
    # Gets the token and test user
    access_token, test_user = create_test_user

    # Generate an authentication token for the test user
    access_token = create_access_token(data={"sub": test_user.email})

    # Prepare product data
    product_data = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 100.0,
        "stock_quantity": 50,
        "image_url": "http://example.com/product.jpg",
        "category_id": str(create_category.id),
        "user_id": str(test_user.id)
    }

    headers = {"Authorization": f"Bearer {access_token}"}

    # Create the product
    response_create = client.post("/api/v1/products/", json=product_data, headers=headers)
    created_product = response_create.json()

    # Make a request to delete the product
    response_delete = client.delete(f"/api/v1/products/{created_product['id']}", headers=headers)

    print(f"Response status code: {response_delete.status_code}")
    print(f"Response content: {response_delete.content}")

    # Ensure the deletion request was successful
    assert response_delete.status_code == 200

    # Try to retrieve the deleted product (should return 404)
    response_get = client.get(f"/api/v1/products/{created_product['id']}", headers=headers)

    print(f"Response status code after deletion: {response_get.status_code}")

    # Ensure the product no longer exists
    assert response_get.status_code == 404

def test_create_category(client, create_test_user):
    """
    Test creating a category.

    - **Steps**:
        1. Creates a test user and generates an access token.
        2. Sends a POST request to create a new category.
        3. Verifies if the response status is 200 (OK) and if the category data is correct.
    """
    # Gets the token and test user
    access_token, test_user = create_test_user

    # Generates a valid access token
    access_token = create_access_token(data={"sub": test_user.email})

    # Data for the new category
    category_data = {
        "name": "Test Category",
        "description": "This is a test category"
    }

    # Headers with the authentication token
    headers = {"Authorization": f"Bearer {access_token}"}

    # Make the request to create the category
    response = client.post("/api/v1/products/categories", json=category_data, headers=headers)

    # Debug: Displays the status code and content of the response
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.content}")

    # Checks whether the request was successful (status code 200)
    if response.status_code == 422:
        print("Validation error details:", response.json())
    assert response.status_code == 200

    # Checks whether the created category data is correct
    response_json = response.json()
    assert response_json["name"] == category_data["name"]
    assert response_json["description"] == category_data["description"]

def test_read_category(client, create_test_user, create_category):
    """
    Test reading a specific category.

    - **Steps**:
        1. Creates a test user and generates an access token.
        2. Creates a test category.
        3. Sends a GET request to read the category.
        4. Verifies if the response status is 200 (OK) and if the category data is correct.
    """
    # Gets the token and test user
    access_token, test_user = create_test_user

    # Generates a valid access token
    access_token = create_access_token(data={"sub": test_user.email})

    # Create a test category
    category = create_category

    # Headers with the authentication token
    headers = {"Authorization": f"Bearer {access_token}"}

    # Make a request to read the specific category
    response = client.get(f"/api/v1/products/categories/{category.id}", headers=headers)

    # Debug: Displays the status code and content of the response
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.content}")

    # Checks whether the request was successful (status code 200)
    assert response.status_code == 200

    # Checks if the response contains JSON
    response_json = response.json()
    print(f"Response JSON: {response_json}")  # Debug: Display the full JSON

    # Checks whether the returned category data is correct
    assert "id" in response_json, "Field 'id' not found in response"
    assert response_json["id"] == str(category.id)  # Convert UUID to string

    assert "description" in response_json, "Field 'description' not found in response"
    assert response_json["description"] == category.description

    # Check additional fields if necessary
    assert "date_creation" in response_json, "Field 'date_creation' not found in response"
    assert "date_update" in response_json, "Field 'date_update' not found in response"

def test_delete_category(client, create_test_user, create_category):
    """
    Test deleting a category.

    - **Steps**:
        1. Creates a test user and generates an access token.
        2. Creates a test category.
        3. Sends a DELETE request to delete the category.
        4. Verifies if the response status is 200 (OK) and if the category no longer exists.
    """
    # Gets the token and test user
    access_token, test_user = create_test_user

    # Generates a valid access token
    access_token = create_access_token(data={"sub": test_user.email})

    # Create a test category
    category = create_category

    # Headers with the authentication token
    headers = {"Authorization": f"Bearer {access_token}"}

    # Make the request to delete the category
    response_delete = client.delete(f"/api/v1/products/categories/{category.id}", headers=headers)

    # Debug: Displays the status code and content of the response
    print(f"Response status code: {response_delete.status_code}")
    print(f"Response content: {response_delete.content}")

    # Checks whether the request was successful (status code 200)
    assert response_delete.status_code == 200

    # Attempts to recover the deleted category (should return 404)
    response_get = client.get(f"/api/v1/products/categories/{category.id}", headers=headers)

    # Debug: Display status code after deletion
    print(f"Response status code after deletion: {response_get.status_code}")

    # Checks if the category no longer exists
    assert response_get.status_code == 404
