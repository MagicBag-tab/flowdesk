from sqlalchemy.orm import Session
from app.models.product import Product
from app.utils.exceptions import NotFoundError, ValidationError

def create_product(db: Session, data):
    if not data.nombre.strip():
        raise ValidationError("El nombre del producto no puede estar vacío")
    
    if not data.estado.strip():
        raise ValidationError("El estado del producto no puede estar vacío")
    
    product = Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_products(db: Session):
    return db.query(Product).all()

#Cambios en stock y validacion
def validate_stock(stock_actual, cambio):
    new_stock = stock_actual + cambio

    if new_stock < 0 :
        raise ValidationError("stock insuficiente")
    
    return new_stock

#Actualización del stock en db
def update_stock(db: Session, product_id: int, data):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise NotFoundError("Producto no encontrado")
    
    product.stock_actual = validate_stock(product.stock_actual, data.cantidad)

    db.commit()
    db.refresh(product)

    return product