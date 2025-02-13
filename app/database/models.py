from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, UTC
from app.database.connection import Base


class User(Base):
    """
    Represents a user in the system.

    - **id**: Unique identifier (UUID).
    - **name**: User's full name.
    - **email**: Unique email address.
    - **password**: Hashed password.
    - **date_creation**: Timestamp of user creation.
    - **date_update**: Timestamp of last update.
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    date_creation = Column(DateTime, default=lambda: datetime.now(UTC))
    date_update = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))


class Product(Base):
    """
    Represents a product in the inventory.

    - **id**: Unique identifier (UUID).
    - **name**: Product name.
    - **description**: Detailed description of the product.
    - **price**: Product price (must be greater than zero).
    - **stock_quantity**: Quantity available in stock (must be positive).
    - **image_url**: Optional URL of the product image.
    - **category_id**: Foreign key referencing the category.
    - **user_id**: Foreign key referencing the user who added the product.
    - **date_creation**: Timestamp of product creation.
    - **date_update**: Timestamp of last update.
    """
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    image_url = Column(String)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    date_creation = Column(DateTime, default=lambda: datetime.now(UTC))
    date_update = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))


class Category(Base):
    """
    Represents a product category.

    - **id**: Unique identifier (UUID).
    - **name**: Category name.
    - **description**: Optional category description.
    - **date_creation**: Timestamp of category creation.
    - **date_update**: Timestamp of last update.
    """
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    name = Column(String, nullable=False)
    description = Column(String)
    date_creation = Column(DateTime, default=lambda: datetime.now(UTC))
    date_update = Column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))


class InventoryTransaction(Base):
    """
    Represents an inventory transaction (stock movement).

    - **id**: Unique identifier (UUID).
    - **product_id**: Foreign key referencing the product.
    - **type**: Transaction type (e.g., "incoming", "outgoing").
    - **quantity**: Quantity of products moved.
    - **date_transaction**: Timestamp of the transaction.
    - **description**: Optional description of the transaction.
    """
    __tablename__ = "inventory_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    type = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    date_transaction = Column(DateTime, default=lambda: datetime.now(UTC))
    description = Column(String)
