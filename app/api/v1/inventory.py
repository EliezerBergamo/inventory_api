from fastapi import  APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.utils.auth import get_current_user
from app.database.models import User
from app.schemas.item_schemas import (
    ProductCreate,
    ProductResponse,
    InventoryTransactionCreate,
    InventoryTransactionResponse,
    CategoryCreate,
    CategoryResponse
)
from app.services.inventory_service import (
    create_product,
    get_products,
    get_product,
    update_product,
    delete_product,
    create_inventory_transaction,
    get_inventory_transactions,
    get_inventory_transaction,
    create_category,
    get_categories,
    get_category,
    update_category,
    delete_category
)

router = APIRouter(prefix="/products", tags=["products"])

# Endpoint for creating a product
@router.post("/", response_model=ProductResponse)
def create_new_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new product in the inventory.

    - **Parameters**:
        - `product`: ProductCreate schema containing product details.
        - `db`: Database session dependency.
        - `current_user`: The authenticated user (retrieved via JWT token).

    - **Returns**:
        - ProductResponse schema with the newly created product's details.

    - **Raises**:
        - HTTPException (400): If the product data is invalid.
    """
    try:
        new_product = create_product(db, product, current_user.id)
        return new_product
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

# Endpoint to list all products
@router.get("/", response_model=List[ProductResponse])
def list_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    List all products in the inventory.

    - **Parameters**:
        - `skip`: Number of products to skip (for pagination).
        - `limit`: Maximum number of products to return (for pagination).
        - `db`: Database session dependency.

    - **Returns**:
        - A list of ProductResponse schemas.
    """
    products = get_products(db, skip=skip, limit=limit)
    return products

# Endpoint to query a specific product
@router.get("/{product_id}", response_model=ProductResponse)
def read_product(
        product_id: str,
        db: Session = Depends(get_db)
):
    """
    Retrieve details of a specific product.

    - **Parameters**:
        - `product_id`: The ID of the product to retrieve.
        - `db`: Database session dependency.

    - **Returns**:
        - ProductResponse schema with the product's details.

    - **Raises**:
        - HTTPException (404): If the product is not found.
    """
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product

# Endpoint for editing a product
@router.put("/{product_id}", response_model=ProductResponse)
def update_existing_product(
        product_id: str,
        product: ProductCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Update an existing product in the inventory.

    - **Parameters**:
        - `product_id`: The ID of the product to update.
        - `product`: ProductCreate schema containing updated product details.
        - `db`: Database session dependency.
        - `current_user`: The authenticated user (retrieved via JWT token).

    - **Returns**:
        - ProductResponse schema with the updated product's details.

    - **Raises**:
        - HTTPException (404): If the product is not found.
    """
    try:
        updated_product = update_product(db, product_id, product)
        return updated_product
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

# Endpoint to delete a product
@router.delete("/{product_id}", response_model=ProductResponse)
def delete_existing_product(
        product_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Delete an existing product from the inventory.

    - **Parameters**:
        - `product_id`: The ID of the product to delete.
        - `db`: Database session dependency.
        - `current_user`: The authenticated user (retrieved via JWT token).

    - **Returns**:
        - ProductResponse schema with the deleted product's details.

    - **Raises**:
        - HTTPException (404): If the product is not found.
    """
    try:
        deleted_product = delete_product(db, product_id)
        return deleted_product
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

# Endpoint for recording a stock movement
@router.post("/{product_id}/transactions", response_model=InventoryTransactionResponse)
def create_transaction(
        product_id: str,
        transaction: InventoryTransactionCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Record a stock movement for a specific product.

    - **Parameters**:
        - `product_id`: The ID of the product associated with the transaction.
        - `transaction`: InventoryTransactionCreate schema containing transaction details.
        - `db`: Database session dependency.
        - `current_user`: The authenticated user (retrieved via JWT token).

    - **Returns**:
        - InventoryTransactionResponse schema with the recorded transaction's details.

    - **Raises**:
        - HTTPException (400): If the transaction data is invalid.
    """
    try:
        new_transaction = create_inventory_transaction(db, product_id, transaction, current_user.id)
        return new_transaction
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

# Endpoint to list all stock movements of a product
@router.get("/{product_id}/transactions", response_model=List[InventoryTransactionResponse])
def list_transactions(
        product_id: str,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
):
    """
    List all stock movements for a specific product.

    - **Parameters**:
        - `product_id`: The ID of the product to retrieve transactions for.
        - `skip`: Number of transactions to skip (for pagination).
        - `limit`: Maximum number of transactions to return (for pagination).
        - `db`: Database session dependency.

    - **Returns**:
        - A list of InventoryTransactionResponse schemas.
    """
    transactions = get_inventory_transactions(db, product_id, skip=skip, limit=limit)
    return transactions

# Endpoint to query a specific stock movement
@router.get("/{product_id}/transactions/{transaction_id}", response_model=InventoryTransactionResponse)
def read_transaction(
        product_id: str,
        transaction_id: str,
        db: Session = Depends(get_db),
):
    """
    Retrieve details of a specific stock movement.

    - **Parameters**:
        - `product_id`: The ID of the product associated with the transaction.
        - `transaction_id`: The ID of the transaction to retrieve.
        - `db`: Database session dependency.

    - **Returns**:
        - InventoryTransactionResponse schema with the transaction's details.

    - **Raises**:
        - HTTPException (404): If the transaction is not found.
    """
    transaction = get_inventory_transaction(db, product_id, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock movement not found",
        )
    return transaction

# Endpoint for creating a category
@router.post("/categories", response_model=CategoryCreate)
def create_new_category(
        category: CategoryCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Create a new category for products.

    - **Parameters**:
        - `category`: CategoryCreate schema containing category details.
        - `db`: Database session dependency.
        - `current_user`: The authenticated user (retrieved via JWT token).

    - **Returns**:
        - CategoryCreate schema with the newly created category's details.

    - **Raises**:
        - HTTPException (400): If the category data is invalid.
    """
    try:
        new_category = create_category(db, category)
        return new_category
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# Endpoint to list all categories
@router.get("/categories", response_model=List[CategoryResponse])
def list_categories(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
):
    """
    List all categories in the inventory.

    - **Parameters**:
        - `skip`: Number of categories to skip (for pagination).
        - `limit`: Maximum number of categories to return (for pagination).
        - `db`: Database session dependency.

    - **Returns**:
        - A list of CategoryResponse schemas.
    """
    categories = get_categories(db, skip=skip, limit=limit)
    return categories

# Endpoint to query a specific category
@router.get("/categories/{category_id}", response_model=CategoryResponse)
def read_category(
        category_id: str,
        db: Session = Depends(get_db),
):
    """
    Retrieve details of a specific category.

    - **Parameters**:
        - `category_id`: The ID of the category to retrieve.
        - `db`: Database session dependency.

    - **Returns**:
        - CategoryResponse schema with the category's details.

    - **Raises**:
        - HTTPException (404): If the category is not found.
    """
    category = get_category(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category

# Endpoint for editing a category
@router.put("/categories/{category_id}", response_model=CategoryResponse)
def update_existing_category(
        category_id: str,
        category: CategoryCreate,
        db: Session = Depends(get_db),
):
    """
    Update an existing category.

    - **Parameters**:
        - `category_id`: The ID of the category to update.
        - `category`: CategoryCreate schema containing updated category details.
        - `db`: Database session dependency.

    - **Returns**:
        - CategoryResponse schema with the updated category's details.

    - **Raises**:
        - HTTPException (404): If the category is not found.
    """
    try:
        updated_category = update_category(db, category_id, category)
        return updated_category
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

# Endpoint to delete a category
@router.delete("/categories/{category_id}", response_model=CategoryResponse)
def delete_existing_category(
        category_id: str,
        db: Session = Depends(get_db),
):
    """
    Delete an existing category.

    - **Parameters**:
        - `category_id`: The ID of the category to delete.
        - `db`: Database session dependency.

    - **Returns**:
        - CategoryResponse schema with the deleted category's details.

    - **Raises**:
        - HTTPException (404): If the category is not found.
    """
    try:
        deleted_category = delete_category(db, category_id)
        return deleted_category
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
