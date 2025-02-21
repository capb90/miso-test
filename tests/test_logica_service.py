import unittest
from datetime import datetime, time

from src.logica.logica_service import LogicaService
from src.modelo.declarative_base import Session, session
from src.modelo.persona import Persona
from src.modelo.ejercicio import Ejercicio
from src.modelo.entrenamiento import Entrenamiento
import src.modelo.declarative_base


class LogicaServiceTestCase(unittest.TestCase):

    def setUp(self):
        src.modelo.declarative_base.IS_TEST = True
        self.logica = LogicaService()

        #Creacion datos de prueba
        self.session = Session()

        #Crear personas de prueba
        persona1 = Persona(nombre="John",apellidos="Doe",fecha_inicio=datetime.today(),talla=176,peso=75,edad=32,medida_brazo=15,medida_pecho=80,medida_cintura=60,medida_pierna=70,medida_abdomen=50)
        persona2 = Persona(nombre="Angelica",apellidos="Mora",fecha_inicio=datetime.today(),talla=156,peso=50,edad=22,medida_brazo=10,medida_pecho=50,medida_cintura=60,medida_pierna=30,medida_abdomen=40)
        persona3 = Persona(nombre="Juan",apellidos="Doe",fecha_inicio=datetime.today(),talla=190,peso=80,edad=40,medida_brazo=20,medida_pecho=90,medida_cintura=70,medida_pierna=40,medida_abdomen=60)
        persona4 = Persona(nombre="Andres",apellidos="Lopez",fecha_inicio=datetime.today(),talla=160,peso=70,edad=28,medida_brazo=30,medida_pecho=80,medida_cintura=70,medida_pierna=30,medida_abdomen=70)

        self.session.add(persona1)
        self.session.add(persona2)
        self.session.add(persona3)
        self.session.add(persona4)


        #Creacion Ejercicios
        ejercicio1 = Ejercicio(nombre="Press de banca",descripcion="Lorem ipsum",calorias=80,enlace_video="https://ejercicio_1.com")
        ejercicio2 = Ejercicio(nombre="Sentadilla",descripcion="Lorem ipsum",calorias=160,enlace_video="https://ejercicio_2.com")
        ejercicio3 = Ejercicio(nombre="Remo con barra T",descripcion="Lorem ipsum",calorias=110,enlace_video="https://ejercicio_3.com")
        ejercicio4 = Ejercicio(nombre="Press Militar",descripcion="Lorem ipsum",calorias=90,enlace_video="https://ejercicio_4.com")

        self.session.add(ejercicio1)
        self.session.add(ejercicio2)
        self.session.add(ejercicio3)
        self.session.add(ejercicio4)


        #Creacion Entrenamientos

        entrenamiento1 = Entrenamiento(fecha=datetime(2024, 8, 25),cat_repeticiones=12,tiempo=time(hour=0, minute=10, second=2))
        entrenamiento2 = Entrenamiento(fecha=datetime(2024, 11, 21),cat_repeticiones=8,tiempo=time(hour=0, minute=5, second=2))
        entrenamiento3 = Entrenamiento(fecha=datetime(2024, 12, 21), cat_repeticiones=5,tiempo=time(hour=0, minute=8, second=0))
        entrenamiento4 = Entrenamiento(fecha=datetime(2024, 10, 27), cat_repeticiones=15,tiempo=time(hour=0, minute=12, second=0))
        self.session.add(entrenamiento1)
        self.session.add(entrenamiento2)
        self.session.add(entrenamiento3)
        self.session.add(entrenamiento4)

        persona1.entrenamientos = [entrenamiento1]
        ejercicio1.entrenamientos = [entrenamiento1]

        persona2.entrenamientos = [entrenamiento2]
        ejercicio2.entrenamientos = [entrenamiento2]

        persona3.entrenamientos = [entrenamiento3]
        ejercicio3.entrenamientos = [entrenamiento3]

        persona4.entrenamientos = [entrenamiento4]
        ejercicio4.entrenamientos = [entrenamiento4]


        self.session.commit()



    def tearDown(self):
        self.session.query(Entrenamiento).delete()
        self.session.query(Ejercicio).delete()
        self.session.query(Persona).delete()
        self.session.commit()
        self.session.close()
        self.logica = None

    def test_dar_personas_listado(self):
        personas = self.logica.dar_personas()
        self.assertIsInstance(personas, list)


    def test_dar_persona_listado_no_vacio(self):
        personas = self.logica.dar_personas()
        self.assertNotEqual(len(personas), 0 )

    def test_dar_personas_organizado(self):
        personas = self.logica.dar_personas()
        self.assertEqual(personas,sorted(personas,key=lambda p: p.nombre))
    
    def test_dar_entrenamientos_listado(self):
        entrenamientos = self.logica.dar_entrenamientos(1)
        self.assertIsInstance(entrenamientos, list)
    
    def test_dar_entrenameintos_listado_no_vacio(self):
        entrenamientos = self.logica.dar_entrenamientos(1)
        self.assertNotEqual(len(entrenamientos), 0 )
    
    def test_regresar_entrenamientos(self):
        entrenamientos = self.logica.dar_entrenamientos(1)
        entreno = entrenamientos[0]
        ejercicio_id = entreno.ejercicio
        nombre_ejercicio = self.session.get(Ejercicio,ejercicio_id).nombre
        self.assertEqual(nombre_ejercicio, "Press de banca")

    def test_comprobar_asociacion_entrenamientos(self):
        entrenamientos = self.logica.dar_entrenamientos(1)
        self.assertTrue(all(ent.persona==1 for ent in entrenamientos))
    
    def test_dar_entrenamientos_organizado(self):
        entrenamientos = self.logica.dar_entrenamientos(1)
        self.assertEqual(entrenamientos,sorted(entrenamientos,key=lambda p: p.fecha))

    def test_cantidad_entrenamientos(self):
        self.logica.crear_entrenamiento(None,None,datetime(2025, 2, 20),12,time(hour=0, minute=10, second=2))
        entrenamientos = self.session.query(Entrenamiento).all()
        self.assertEqual(len(entrenamientos),5)