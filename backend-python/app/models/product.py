from sqlalchemy import Column, Integer, String, Float, Numeric, Text, ForeignKey
from app.db.database import Base

class Product(Base):
    _tablename_ = "producto"
    id_producto = Column(Integer, primary_key = True, index = True)
    id_proveedor = Column(Integer, ForeignKey("proveedor.id_proveedor"), nullable = True)
    nombre = Column(String(100), nullable = False)
    descripcion = Column(Text, nullable = True)
    precio = Column(Numeric(10, 2), nullable = False)
    stock_actual = Column(Integer, nullable = False, default = 0)
    stock_minimo = Column(Integer, nullable = False, default = 0)
    estado = Column(String(30), nullable = False)