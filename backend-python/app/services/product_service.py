from sqlalchemy.orm import Session
from app.models.product import Product
from app.utils.exceptions import NotFoundError, ValidationError

def create_product(db: Session, data):
    product = Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_products(db: Session):
    return db.query(Product).all()

#Cambios en stock y validacion
def validate_stock(current_stock, change):
    new_stock = current_stock + change

    if new_stock < 0 :
        raise ValidationError("stock insuficiente")
    
    return new_stock

#Actualización del stock en db
def update_stock(db: Session, product_id: int, data):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise NotFoundError("Producto no encontrado")
    
    product.stock = validate_stock(product.stock, data.quantity)

    db.commit()
    db.refresh(product)

    return product