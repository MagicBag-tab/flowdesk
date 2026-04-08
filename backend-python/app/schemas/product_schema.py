from pydantic import BaseModel, validator
from typíng import Optional

class ProductCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock_actual: int = 0
    stock_minimo: int = 0
    estado: str
    id_proveedor: Optional[int] = None

    #Validar "nombre"
    def nombre_valido(cls, v):
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v
    
    #Validar "estado"
    def estado_valido(cls, v):
        estados_validos = ["disponible", "agotado", "descontinuado"]
        if v not in estados_validos:
            raise ValueError(f"El estado debe ser uno de: {', '.join(estados_validos)}")
        return v

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