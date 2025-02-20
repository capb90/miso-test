import enum

from sqlalchemy import Column, Integer, String, DATETIME, Enum, Float
from sqlalchemy.orm import relationship
from .entrenamiento import Entrenamiento
from .declarative_base import Base


class Estado(enum.Enum):
    ACTIVA=1
    INACTIVA=2

class Persona(Base):
    __tablename__ = 'persona'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellidos = Column(String)
    fecha_inicio = Column(DATETIME)
    talla = Column(Integer)
    peso = Column(Integer)
    edad = Column(Integer)
    razon_fin =Column(String, nullable=True)
    fecha_fin = Column(DATETIME,nullable=True)
    estado = Column(Enum(Estado),default=Estado.ACTIVA)
    medida_brazo = Column(Float)
    medida_pecho = Column(Float)
    medida_cintura = Column(Float)
    medida_pierna = Column(Float)
    medida_abdomen = Column(Float)
    entrenamientos = relationship('Entrenamiento', cascade='all,delete,delete-orphan')