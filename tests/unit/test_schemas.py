from app.schemas.item_schemas import ProductCreate, CategoryCreate
from pydantic import ValidationError
from uuid import uuid4
import pytest

# Valid UUIDs for testing
valid_category_id = uuid4()
valid_user_id = uuid4()

def test_product_create_schema():
    """
    Test the `ProductCreate` schema with valid data.

    - **Steps**:
        1. Creates a dictionary with valid product data.
        2. Instantiates the `ProductCreate` schema with the data.
        3. Verifies if the schema fields match the input data.

    - **Assertions**:
        - The `name` and `price` fields should match the input data.
    """
    # Valid data
    valid_data = {
        "name": "Product Test",
        "description": "Product Description Test",
        "price": 29.99,
        "stock_quantity": 100,
        "image_url": "http://example.com/image.jpg",
        "category_id": valid_category_id,
        "user_id": valid_user_id
    }

    # Create the schema
    product = ProductCreate(**valid_data)

    # Check the data
    assert product.name == "Product Test"
    assert product.price == 29.99

def test_category_create_schema():
    """
    Test the `CategoryCreate` schema with valid data.

    - **Steps**:
        1. Creates a dictionary with valid category data.
        2. Instantiates the `CategoryCreate` schema with the data.
        3. Verifies if the schema fields match the input data.

    - **Assertions**:
        - The `name` and `description` fields should match the input data.
    """
    # Valid data
    valid_data = {
        "name": "Test Category",
        "description": "Test Category Description"
    }

    # Create the schema
    category = CategoryCreate(**valid_data)

    # Check the data
    assert category.name == "Test Category"
    assert category.description == "Test Category Description"

def test_product_create_edge_cases():
    """
    Test edge cases for the `ProductCreate` schema.

    - **Test Cases**:
        1. Negative price (should raise `ValidationError`).
        2. Zero stock quantity (should raise `ValidationError`).
        3. Empty name (should raise `ValidationError`).
        4. Invalid URL (should raise `ValidationError`).

    - **Assertions**:
        - Each invalid case should raise a `ValidationError`.
    """
    # Test with negative price (should fail)
    invalid_data = {
        "name": "Product Test",
        "description": "Product Description Test",
        "price": -10.0,  # Invalid price
        "stock_quantity": 100,
        "image_url": "http://example.com/image.jpg",
        "category_id": valid_category_id
    }

    with pytest.raises(ValidationError):
        ProductCreate(**invalid_data)

    # Test with zero stock quantity (should fail)
    invalid_data = {
        "name": "Product Test",
        "description": "Product Description Test",
        "price": 29.99,
        "stock_quantity": 0, # Zero quantity
        "image_url": "http://example.com/image.jpg",
        "category_id": valid_category_id
    }

    with pytest.raises(ValidationError):
        ProductCreate(**invalid_data)

    # Test with empty name (should fail)
    invalid_data = {
        "name": "", # Empty name
        "description": "Product Description Test",
        "price": 29.99,
        "stock_quantity": 100,
        "image_url": "http://example.com/image.jpg",
        "category_id": valid_category_id
    }

    with pytest.raises(ValidationError):
        ProductCreate(**invalid_data)

    # Test with invalid URL (should fail)
    invalid_data = {
        "name": "Product Test",
        "description": "Product Description Test",
        "price": 29.99,
        "stock_quantity": 100,
        "image_url": "invalid-url", # Invalid URL
        "category_id": valid_category_id
    }

    with pytest.raises(ValidationError):
        ProductCreate(**invalid_data)
