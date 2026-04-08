from sqlalchemy import Session
from app.service import product_service

def create_product(db: Session, product):
    return product_service.create_product(db, product)

def get_products(db: Session):
    return product_service.get_product(db)

def update_stock(db: Session, product_id: int, data):
    return product_service.update_stock(db, product_id, data)