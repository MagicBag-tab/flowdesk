from pydantic import BaseModel, validator

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int

    #Validar "price"
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        return v
    
    #Validar "stock"
    def stock_not_negative(cls, v): 
        if v < 0:
            raise ValueError("El stock no puede ser negativo")
        return v
    
class UpdateStock(BaseModel):
    quantity: int