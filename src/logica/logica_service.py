'''
Esta clase es tan sólo un mock con datos para probar la interfaz
'''
from src.logica.FachadaEnForma import FachadaEnForma
from src.modelo.declarative_base import Base, session, engine
from src.modelo.entrenamiento import Entrenamiento
from src.modelo.persona import Persona


class LogicaService(FachadaEnForma):


    def __init__(self):
        Base.metadata.create_all(engine)



    def dar_personas(self):
        lista_personas = session.query(Persona).all()
        lista_personas = sorted(lista_personas,key=lambda p: p.nombre)
        return lista_personas

    def dar_entrenamientos(self, id_persona):
        return session.query(Entrenamiento).all()

    def dar_persona(self, id_persona):
        return
