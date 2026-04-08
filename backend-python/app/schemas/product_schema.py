from pydantic import BaseModel, validator

class ProductCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock_actual: int = 0
    stock_minimo: int = 0
    estado: str
    id_proveedor: Optional[int] = None

    #Validar "precio"
    def price_valido(cls, v):
        if v < 0:
            raise ValueError("El precio no puede ser negativo")
        return v
    
    #Validar "stock" (actual y minimo)
    def stock_valido(cls, v): 
        if v < 0:
            raise ValueError("El stock no puede ser negativo")
        return v
    
class UpdateStock(BaseModel):
    cantidad: int