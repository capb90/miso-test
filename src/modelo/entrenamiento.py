from sqlalchemy import Column, Integer, DATETIME, ForeignKey, Time

from .declarative_base import Base
from .ejercicio import Ejercicio


class Entrenamiento(Base):
    __tablename__ = 'entrenamiento'

    id = Column(Integer, primary_key=True)
    fecha = Column(DATETIME)
    cat_repeticiones = Column(Integer)
    tiempo = Column(Time)
    persona = Column(Integer,ForeignKey('persona.id'))
    ejercicio = Column(Integer,ForeignKey('ejercicio.id'))
