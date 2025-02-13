from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

# Scheme for creating a user
class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    - **Attributes**:
        - `name`: Full name of the user.
        - `email`: Email address of the user (must be unique).
        - `password`: Password for the user account.
    """
    name: str
    email: str
    password: str

# Scheme for returning a user (without password)
class UserResponse(BaseModel):
    """
    Schema for returning user details (excluding sensitive information like password).

    - **Attributes**:
        - `id`: Unique identifier for the user (UUID).
        - `name`: Full name of the user.
        - `email`: Email address of the user.
        - `date_creation`: Timestamp when the user was created.
        - `date_update`: Timestamp when the user was last updated.

    - **Configuration**:
        - `from_attributes=True`: Allows conversion from ORM models to Pydantic models.
    """
    id: UUID
    name: str
    email: str
    date_creation: datetime
    date_update: datetime

    model_config = ConfigDict(from_attributes=True) # Allows conversion of ORM models to Pydantic

# Scheme for creating a category
class CategoryCreate(BaseModel):
    """
    Schema for creating a new category.

    - **Attributes**:
        - `name`: Name of the category.
        - `description`: Optional description of the category.
    """
    name: str
    description: Optional[str] = None

# Scheme for returning a category
class CategoryResponse(BaseModel):
    """
    Schema for returning category details.

    - **Attributes**:
        - `id`: Unique identifier for the category (UUID).
        - `name`: Name of the category.
        - `description`: Optional description of the category.
        - `date_creation`: Timestamp when the category was created.
        - `date_update`: Timestamp when the category was last updated.

    - **Configuration**:
        - `from_attributes=True`: Allows conversion from ORM models to Pydantic models.
    """
    id: UUID
    description: Optional[str] = None
    date_creation: datetime
    date_update: datetime

    model_config = ConfigDict(from_attributes=True)

# Scheme for creating a product
class ProductCreate(BaseModel):
    """
    Schema for creating a new product.

    - **Attributes**:
        - `name`: Name of the product.
        - `description`: Optional description of the product.
        - `price`: Price of the product (must be greater than zero).
        - `stock_quantity`: Quantity of the product in stock (must be greater than zero).
        - `image_url`: Optional URL of the product's image.
        - `category_id`: ID of the category the product belongs to (UUID).
        - `user_id`: ID of the user who created the product (UUID).
    """
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0, description="Price must be greater than zero")
    stock_quantity: int = Field(gt=0, description="The quantity in stock cannot be negative")
    image_url: Optional[str] = None
    category_id: UUID
    user_id: UUID

# Scheme for returning a product
class ProductResponse(BaseModel):
    """
    Schema for returning product details.

    - **Attributes**:
        - `id`: Unique identifier for the product (UUID).
        - `name`: Name of the product.
        - `description`: Optional description of the product.
        - `price`: Price of the product.
        - `stock_quantity`: Quantity of the product in stock.
        - `image_url`: Optional URL of the product's image.
        - `category_id`: ID of the category the product belongs to (UUID).
        - `user_id`: ID of the user who created the product (UUID).
        - `date_creation`: Timestamp when the product was created.
        - `date_update`: Timestamp when the product was last updated.

    - **Configuration**:
        - `from_attributes=True`: Allows conversion from ORM models to Pydantic models.
    """
    id: UUID
    description: Optional[str] = None
    price: float
    stock_quantity: int
    image_url: Optional[str] = None
    category_id: UUID
    user_id: UUID
    date_creation: datetime
    date_update: datetime

    model_config = ConfigDict(from_attributes=True)

# Scheme for creating an inventory transaction
class InventoryTransactionCreate(BaseModel):
    """
    Schema for creating a new inventory transaction.

    - **Attributes**:
        - `product_id`: ID of the product associated with the transaction (UUID).
        - `type`: Type of transaction ("entry" or "exit").
        - `quantity`: Quantity of products involved in the transaction (must be greater than zero).
        - `description`: Optional description of the transaction.
    """
    product_id: UUID
    type: str
    quantity: int = Field(gt=0, description="Quantity must be greater than zero")
    description: Optional[str] = None

# Scheme for returning a stock transaction
class InventoryTransactionResponse(BaseModel):
    """
    Schema for returning inventory transaction details.

    - **Attributes**:
        - `id`: Unique identifier for the transaction (UUID).
        - `product_id`: ID of the product associated with the transaction (UUID).
        - `type`: Type of transaction ("entry" or "exit").
        - `quantity`: Quantity of products involved in the transaction.
        - `date_transaction`: Timestamp when the transaction occurred.
        - `description`: Optional description of the transaction.

    - **Configuration**:
        - `from_attributes=True`: Allows conversion from ORM models to Pydantic models.
    """
    id: UUID
    product_id: UUID
    type: str
    quantity: int
    date_transaction: datetime
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
