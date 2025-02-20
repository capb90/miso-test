from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from src.modelo.declarative_base import Base


class Ejercicio(Base):
    __tablename__ = 'ejercicio'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    descripcion = Column(String)
    calorias = Column(Float)
    enlace_video = Column(String)
    entrenamientos = relationship('Entrenamiento',cascade='all,delete,delete-orphan')

