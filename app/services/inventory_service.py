from sqlalchemy.orm import Session
from app.database.models import (
    Product,
    Category,
    InventoryTransaction
)
from app.schemas.item_schemas import (
    ProductCreate,
    InventoryTransactionCreate,
    CategoryCreate
)

# Function to create a product
def create_product(db: Session, product: ProductCreate, user_id: str):
    """
    Creates a new product in the database.

    - **Parameters**:
        - `db`: Database session.
        - `product`: ProductCreate schema containing product details.
        - `user_id`: ID of the user creating the product.

    - **Returns**:
        - The newly created product.

    - **Raises**:
        - ValueError: If the category does not exist.
    """
    # Checks if the category exists
    db_category = db.query(Category).filter(Category.id == product.category_id).first()
    if not db_category:
        raise ValueError("Category not found")

    # Create the product
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock_quantity=product.stock_quantity,
        image_url=product.image_url,
        category_id=product.category_id,
        user_id=user_id,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

# Function to list all products
def get_products(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieves a list of products from the database.

    - **Parameters**:
        - `db`: Database session.
        - `skip`: Number of products to skip (for pagination).
        - `limit`: Maximum number of products to return (for pagination).

    - **Returns**:
        - A list of products.
    """
    return db.query(Product).offset(skip).limit(limit).all()

# Function to get a product by ID
def get_product(db: Session, product_id: str):
    """
    Retrieves a specific product by its ID.

    - **Parameters**:
        - `db`: Database session.
        - `product_id`: ID of the product to retrieve.

    - **Returns**:
        - The product if found, otherwise None.
    """
    return db.query(Product).filter(Product.id == product_id).first()

# Function to update a product
def update_product(db: Session, product_id: str, product: ProductCreate):
    """
    Updates an existing product in the database.

    - **Parameters**:
        - `db`: Database session.
        - `product_id`: ID of the product to update.
        - `product`: ProductCreate schema containing updated product details.

    - **Returns**:
        - The updated product.

    - **Raises**:
        - ValueError: If the product is not found.
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise ValueError("Product not found")

    # Updates product fields
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.stock_quantity = product.stock_quantity
    db_product.image_url = product.image_url
    db_product.category_id = product.category_id

    db.commit()
    db.refresh(db_product)

    return db_product

# Function to delete a product
def delete_product(db: Session, product_id: str):
    """
    Deletes an existing product from the database.

    - **Parameters**:
        - `db`: Database session.
        - `product_id`: ID of the product to delete.

    - **Returns**:
        - The deleted product.

    - **Raises**:
        - ValueError: If the product is not found.
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise ValueError("Product not found")

    db.delete(db_product)
    db.commit()

    return db_product

# Function to create a stock movement
def create_inventory_transaction(
        db: Session, product_id: str, transaction: InventoryTransactionCreate, user_id: str
):
    """
    Creates a new inventory transaction for a product.

    - **Parameters**:
        - `db`: Database session.
        - `product_id`: ID of the product associated with the transaction.
        - `transaction`: InventoryTransactionCreate schema containing transaction details.
        - `user_id`: ID of the user creating the transaction.

    - **Returns**:
        - The newly created inventory transaction.

    - **Raises**:
        - ValueError: If the product is not found or if there is insufficient stock for an "exit" transaction.
    """
    # Check if the product exists
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise ValueError("Product not found")

    # Creates inventory movement
    new_transaction = InventoryTransaction(
        product_id=product_id,
        type=transaction.type,
        quantity=transaction.quantity,
        description=transaction.description,
        user_id=user_id,
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    # Updates the product's stock quantity
    if transaction.type == "entry":
        db_product.stock_quantity += transaction.quantity
    elif transaction.type == "exit":
        if db_product.stock_quantity < transaction.quantity:
            raise ValueError("Insufficient stock quantity")
        db_product.stock_quantity -= transaction.quantity

    db.commit()
    db.refresh(db_product)

    return new_transaction

# Function to list all stock movements of a product
def get_inventory_transactions(
        db: Session, product_id: str, skip: int = 0, limit: int = 100
):
    """
    Retrieves a list of inventory transactions for a specific product.

    - **Parameters**:
        - `db`: Database session.
        - `product_id`: ID of the product to retrieve transactions for.
        - `skip`: Number of transactions to skip (for pagination).
        - `limit`: Maximum number of transactions to return (for pagination).

    - **Returns**:
        - A list of inventory transactions.
    """
    return (
        db.query(InventoryTransaction)
        .filter(InventoryTransaction.product_id == product_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

# Function to get a specific stock movement
def get_inventory_transaction(db: Session, product_id: str, transaction_id: str):
    """
    Retrieves a specific inventory transaction by its ID.

    - **Parameters**:
        - `db`: Database session.
        - `product_id`: ID of the product associated with the transaction.
        - `transaction_id`: ID of the transaction to retrieve.

    - **Returns**:
        - The inventory transaction if found, otherwise None.
    """
    return (
        db.query(InventoryTransaction)
        .filter(
            InventoryTransaction.product_id == product_id,
            InventoryTransaction.id == transaction_id,
        )
    )

# Function to create a category
def create_category(db: Session, category: CategoryCreate):
    """
    Creates a new category in the database.

    - **Parameters**:
        - `db`: Database session.
        - `category`: CategoryCreate schema containing category details.

    - **Returns**:
        - The newly created category.

    - **Raises**:
        - ValueError: If the category already exists.
    """
    # Checks if category already exists
    db_category = db.query(Category).filter(Category.name == category.name).first()
    if db_category:
        raise ValueError("Category already exists")

    # Create the category
    new_category = Category(
        name=category.name,
        description=category.description,
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

# Function to list all categories
def get_categories(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieves a list of categories from the database.

    - **Parameters**:
        - `db`: Database session.
        - `skip`: Number of categories to skip (for pagination).
        - `limit`: Maximum number of categories to return (for pagination).

    - **Returns**:
        - A list of categories.
    """
    return db.query(Category).offset(skip).limit(limit).all()

# Function to get a specific category
def get_category(db: Session, category_id: str):
    """
    Retrieves a specific category by its ID.

    - **Parameters**:
        - `db`: Database session.
        - `category_id`: ID of the category to retrieve.

    - **Returns**:
        - The category if found, otherwise None.
    """
    return db.query(Category).filter(Category.id == category_id).first()

# Function to update a category
def update_category(db: Session, category_id: str, category: CategoryCreate):
    """
    Updates an existing category in the database.

    - **Parameters**:
        - `db`: Database session.
        - `category_id`: ID of the category to update.
        - `category`: CategoryCreate schema containing updated category details.

    - **Returns**:
        - The updated category.

    - **Raises**:
        - ValueError: If the category is not found.
    """
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise ValueError("Category not found")

    # Updates category fields
    db_category.name = category.name
    db_category.description = category.description

    db.commit()
    db.refresh(db_category)

    return db_category

# Function to delete a category
def delete_category(db: Session, category_id: str):
    """
    Deletes an existing category from the database.

    - **Parameters**:
        - `db`: Database session.
        - `category_id`: ID of the category to delete.

    - **Returns**:
        - The deleted category.

    - **Raises**:
        - ValueError: If the category is not found.
    """
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise ValueError("Category not found")

    db.delete(db_category)
    db.commit()

    return db_category
