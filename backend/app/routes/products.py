"""Product routes for VERIFY GH."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductRead, ProductSearch

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductRead)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product (admin only)."""
    # Check if registration number already exists
    existing = db.query(Product).filter(Product.registration_number == product.registration_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Registration number already exists")
    
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/search", response_model=List[ProductRead])
def search_products(
    query: str = Query(..., min_length=1, max_length=512),
    category: str = None,
    db: Session = Depends(get_db),
):
    """Search products by name, registration number, or manufacturer."""
    search_query = f"%{query}%"
    
    products_query = db.query(Product).filter(
        (Product.name.ilike(search_query)) |
        (Product.registration_number.ilike(search_query)) |
        (Product.manufacturer.ilike(search_query))
    )
    
    if category:
        products_query = products_query.filter(Product.category == category)
    
    products = products_query.limit(50).all()
    return products


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a product by ID."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
