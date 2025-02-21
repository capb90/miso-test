'''
Esta clase es tan sólo un mock con datos para probar la interfaz
'''
from src.logica.FachadaEnForma import FachadaEnForma
from src.modelo.declarative_base import Base, Session, session, engine
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
        lista_entrenamientos = session.query(Entrenamiento).filter(Entrenamiento.persona==id_persona).all()
        lista_entrenamientos = sorted(lista_entrenamientos, key=lambda ent: ent.fecha)
        return lista_entrenamientos

    def crear_entrenamiento(self, persona, ejercicio, fecha, repeticiones, tiempo):
        entrenamiento = Entrenamiento(fecha=fecha,cat_repeticiones=repeticiones,tiempo=tiempo)
        entrenamiento.persona = persona.id
        entrenamiento.ejercicio = ejercicio.id
        session.add(entrenamiento)
        session.commit()

    def dar_persona(self, id_persona):
        return
