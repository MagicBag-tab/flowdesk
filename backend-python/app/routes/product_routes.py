from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controllers import product_controller
from app.schemas.product_schema import ProductCreate, UpdateStock
from app.db.database import get_db

router = APIRouter()

#Post products
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return product_controller.create_product(db, product)

#Get products
def get_products(db: Session = Depends(get_db)):
    return product_controller.get_products(db)

#Patch products/id/stock
def update_stock(product_id: int, data: UpdateStock, db: Session = Depends(get_db)):
    return product_controller.update_stock(db, product_id, data)
