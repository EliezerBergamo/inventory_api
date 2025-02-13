import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from app.schemas.item_schemas import (
    ProductCreate,
    InventoryTransactionCreate,
    CategoryCreate
)
from app.services.inventory_service import (
    create_product,
    update_product,
    delete_product,
    create_inventory_transaction,
    create_category,
    update_category,
    delete_category
)

valid_category_id = uuid4()
valid_product_id = uuid4()
valid_user_id = uuid4()

@pytest.fixture
def user_id():
    """
    Fixture to generate a mock user ID.

    - **Returns**:
        - A UUID representing a user ID.
    """
    return uuid4()  # Returns a mock UUID for the user

@pytest.fixture
def db_session():
    """
    Fixture to mock a database session.

    - **Returns**:
        - A MagicMock instance representing a database session.
    """
    # Mocking DB session
    db = MagicMock()
    yield db

@pytest.fixture
def valid_product_data():
    """
    Fixture to generate valid product data for testing.

    - **Returns**:
        - A `ProductCreate` instance with valid data.
    """
    return ProductCreate(
        name="Test Product",
        description="Description of test product",
        price=100.0,
        stock_quantity=10,
        image_url="http://image.url",
        category_id=uuid4(),
        user_id=str(uuid4())  # Adding the user_id here
    )

@pytest.fixture
def valid_inventory_transaction_data():
    """
    Fixture to generate valid inventory transaction data for testing.

    - **Returns**:
        - An `InventoryTransactionCreate` instance with valid data.
    """
    return InventoryTransactionCreate(
        product_id=uuid4(),  # Adding the product_id here
        type="entry",
        quantity=5,
        description="Restocking product"
    )

@pytest.fixture
def valid_category_data():
    """
    Fixture to generate valid category data for testing.

    - **Returns**:
        - A `CategoryCreate` instance with valid data.
    """
    return CategoryCreate(
        name="Test Category",
        description="Description of test category"
    )

def test_create_product(db_session, valid_product_data):
    """
    Test the `create_product` function with valid data.

    - **Steps**:
        1. Mocks the database session to return a valid category.
        2. Calls the `create_product` function with valid product data.
        3. Verifies if the returned product matches the input data.

    - **Assertions**:
        - The product fields should match the input data.
    """
    # Mock category lookup
    db_session.query.return_value.filter.return_value.first.return_value = MagicMock(id=valid_product_data.category_id)

    product = create_product(db_session, valid_product_data, valid_product_data.user_id)  # Passing the user_id

    assert product.name == valid_product_data.name
    assert product.description == valid_product_data.description
    assert product.price == valid_product_data.price
    assert product.stock_quantity == valid_product_data.stock_quantity
    assert product.image_url == valid_product_data.image_url
    assert product.category_id == valid_product_data.category_id

def test_create_product_category_not_found(db_session, valid_product_data):
    """
    Test the `create_product` function when the category is not found.

    - **Steps**:
        1. Mocks the database session to return `None` for the category.
        2. Calls the `create_product` function.
        3. Verifies if a `ValueError` is raised with the message "Category not found".

    - **Assertions**:
        - A `ValueError` should be raised.
    """
    db_session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(ValueError, match="Category not found"):
        create_product(db_session, valid_product_data, str(uuid4()))

def test_update_product(db_session, valid_product_data):
    """
    Test the `update_product` function with valid data.

    - **Steps**:
        1. Mocks the database session to return a valid product.
        2. Calls the `update_product` function with updated product data.
        3. Verifies if the returned product matches the updated data.

    - **Assertions**:
        - The product fields should match the updated data.
        - The database session should commit the changes.
    """
    product_id = uuid4()
    db_product = MagicMock(id=product_id)
    db_session.query.return_value.filter.return_value.first.return_value = db_product

    updated_product_data = valid_product_data.model_copy()
    updated_product_data.name = "Updated Product"

    updated_product = update_product(db_session, str(product_id), updated_product_data)

    assert updated_product.name == "Updated Product"
    db_session.commit.assert_called_once()

def test_update_product_not_found(db_session, valid_product_data):
    """
    Test the `update_product` function when the product is not found.

    - **Steps**:
        1. Mocks the database session to return `None` for the product.
        2. Calls the `update_product` function.
        3. Verifies if a `ValueError` is raised with the message "Product not found".

    - **Assertions**:
        - A `ValueError` should be raised.
    """
    db_session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(ValueError, match="Product not found"):
        update_product(db_session, str(uuid4()), valid_product_data)

def test_delete_product(db_session):
    """
    Test the `delete_product` function.

    - **Steps**:
        1. Mocks the database session to return a valid product.
        2. Calls the `delete_product` function.
        3. Verifies if the returned product matches the deleted product.

    - **Assertions**:
        - The deleted product ID should match the input product ID.
        - The database session should commit the changes.
    """
    product_id = uuid4()
    db_product = MagicMock(id=product_id)
    db_session.query.return_value.filter.return_value.first.return_value = db_product

    deleted_product = delete_product(db_session, str(product_id))

    assert deleted_product.id == product_id
    db_session.commit.assert_called_once()

def test_delete_product_not_found(db_session):
    """
    Test the `delete_product` function when the product is not found.

    - **Steps**:
        1. Mocks the database session to return `None` for the product.
        2. Calls the `delete_product` function.
        3. Verifies if a `ValueError` is raised with the message "Product not found".

    - **Assertions**:
        - A `ValueError` should be raised.
    """
    db_session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(ValueError, match="Product not found"):
        delete_product(db_session, str(uuid4()))

def test_create_inventory_transaction_product_not_found(db_session, valid_inventory_transaction_data):
    """
    Test the `create_inventory_transaction` function when the product is not found.

    - **Steps**:
        1. Mocks the database session to return `None` for the product.
        2. Calls the `create_inventory_transaction` function.
        3. Verifies if a `ValueError` is raised with the message "Product not found".

    - **Assertions**:
        - A `ValueError` should be raised.
    """
    db_session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(ValueError, match="Product not found"):
        create_inventory_transaction(db_session, str(uuid4()), valid_inventory_transaction_data, str(uuid4()))

# Simple class to represent the transaction
class Transaction:
    def __init__(self, id):
        self.id = id

def test_create_category(db_session, valid_category_data):
    """
    Test the `create_category` function with valid data.

    - **Steps**:
        1. Mocks the database session to return `None` for the category (indicating no existing category).
        2. Calls the `create_category` function with valid category data.
        3. Verifies if the returned category matches the input data.

    - **Assertions**:
        - The category fields should match the input data.
    """
    db_session.query.return_value.filter.return_value.first.return_value = None

    category = create_category(db_session, valid_category_data)

    assert category.name == valid_category_data.name
    assert category.description == valid_category_data.description

def test_create_category_already_exists(db_session, valid_category_data):
    """
    Test the `create_category` function when the category already exists.

    - **Steps**:
        1. Mocks the database session to return an existing category.
        2. Calls the `create_category` function.
        3. Verifies if a `ValueError` is raised with the message "Category already exists".

    - **Assertions**:
        - A `ValueError` should be raised.
    """
    db_session.query.return_value.filter.return_value.first.return_value = MagicMock()

    with pytest.raises(ValueError, match="Category already exists"):
        create_category(db_session, valid_category_data)

def test_update_category(db_session, valid_category_data):
    """
    Test the `update_category` function with valid data.

    - **Steps**:
        1. Mocks the database session to return a valid category.
        2. Calls the `update_category` function with updated category data.
        3. Verifies if the returned category matches the updated data.

    - **Assertions**:
        - The category fields should match the updated data.
        - The database session should commit the changes.
    """
    category_id = uuid4()
    db_category = MagicMock(id=category_id)
    db_session.query.return_value.filter.return_value.first.return_value = db_category

    updated_category_data = valid_category_data.model_copy()
    updated_category_data.name = "Updated Category"

    updated_category = update_category(db_session, str(category_id), updated_category_data)

    assert updated_category.name == "Updated Category"
    db_session.commit.assert_called_once()


def test_update_category_not_found(db_session, valid_category_data):
    """
    Test the `update_category` function when the category is not found.

    - **Steps**:
        1. Mocks the database session to return `None` for the category.
        2. Calls the `update_category` function.
        3. Verifies if a `ValueError` is raised with the message "Category not found".

    - **Assertions**:
        - A `ValueError` should be raised.
    """
    db_session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(ValueError, match="Category not found"):
        update_category(db_session, str(uuid4()), valid_category_data)

def test_delete_category(db_session):
    """
    Test the `delete_category` function.

    - **Steps**:
        1. Mocks the database session to return a valid category.
        2. Calls the `delete_category` function.
        3. Verifies if the returned category matches the deleted category.

    - **Assertions**:
        - The deleted category ID should match the input category ID.
        - The database session should commit the changes.
    """
    category_id = uuid4()
    db_category = MagicMock(id=category_id)
    db_session.query.return_value.filter.return_value.first.return_value = db_category

    deleted_category = delete_category(db_session, str(category_id))

    assert deleted_category.id == category_id
    db_session.commit.assert_called_once()


def test_delete_category_not_found(db_session):
    """
    Test the `delete_category` function when the category is not found.

    - **Steps**:
        1. Mocks the database session to return `None` for the category.
        2. Calls the `delete_category` function.
        3. Verifies if a `ValueError` is raised with the message "Category not found".

    - **Assertions**:
        - A `ValueError` should be raised.
    """
    db_session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(ValueError, match="Category not found"):
        delete_category(db_session, str(uuid4()))
