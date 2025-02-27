'''
Esta clase es tan sólo un mock con datos para probar la interfaz
'''
from wsgiref.util import request_uri

from src.logica.FachadaEnForma import FachadaEnForma
from src.modelo.declarative_base import Base, Session, session, engine
from src.modelo.entrenamiento import Entrenamiento
from src.modelo.persona import Persona
from datetime import time

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
        if not isinstance(tiempo, time):
            raise ValueError('El formato de tiempo no es el correcto')
        if persona is None or ejercicio is None :
            raise ValueError('El entrenamiento no puede ser generado')
        entrenamiento = Entrenamiento(fecha=fecha,cat_repeticiones=repeticiones,tiempo=tiempo)
        entrenamiento.persona = persona.id
        entrenamiento.ejercicio = ejercicio.id
        session.add(entrenamiento)
        session.commit()

    def validar_crear_editar_ejercicio(self, nombre, descripcion, enlace, calorias):
        if nombre is None:
            return "El nombre es obligatorio"
        if descripcion is None:
            return "La descripcion es obligatoria"

    def dar_persona(self, id_persona):
        return
