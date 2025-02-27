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
        nombre_ejercicio = self.session.query(Ejercicio).get(ejercicio_id).nombre
        self.assertEqual(nombre_ejercicio, "Press de banca")

    def test_comprobar_asociacion_entrenamientos(self):
        entrenamientos = self.logica.dar_entrenamientos(1)
        self.assertTrue(all(ent.persona==1 for ent in entrenamientos))
    
    def test_dar_entrenamientos_organizado(self):
        entrenamientos = self.logica.dar_entrenamientos(1)
        self.assertEqual(entrenamientos,sorted(entrenamientos,key=lambda p: p.fecha))

    def test_crear_entrenamientos_sin_asignacion(self):
        with self.assertRaises(ValueError) as context:
            self.logica.crear_entrenamiento(None, None, datetime(2025, 2, 20), 12, time(hour=0, minute=10, second=2))

        self.assertEqual(str(context.exception), "El entrenamiento no puede ser generado")

    def test_asignacion_entrenamientos(self):
        persona1 = self.session.query(Persona).get(1)
        ejercicio1 = self.session.query(Ejercicio).get(1)
        self.logica.crear_entrenamiento(persona1, ejercicio1, datetime(2025, 2, 20), 12, time(hour=0, minute=10, second=2))
        entrenamientos_asignados = self.session.query(Entrenamiento).order_by(Entrenamiento.id.desc()).first()
        self.assertEqual(entrenamientos_asignados.persona,1)
        self.assertEqual(entrenamientos_asignados.ejercicio,1)

    def test_validacion_formato_tiempo(self):
        persona1 = self.session.query(Persona).get(1)
        ejercicio1 = self.session.query(Ejercicio).get(1)
        with self.assertRaises(ValueError) as context:
            self.logica.crear_entrenamiento(persona1, ejercicio1, datetime(2025, 2, 20), 12, None)

        self.assertEqual(str(context.exception), "El formato de tiempo no es el correcto")

    def test_validar_crear_ejercicio(self):
        try:
            self.logica.validar_crear_editar_ejercicio("Sentadilla", "Lorem ipsum", "https://ejercicio.com", 160)
        except ValueError as context:
            self.fail(f"Error en el metodo validar_crear_editar_ejercicio: {context}")

    def test_validar_crear_ejercicio_nombre(self):
        response = self.logica.validar_crear_editar_ejercicio(None, "Lorem ipsum", "https://ejercicio.com", 160)
        self.assertEqual(response, "El nombre es obligatorio")

    def test_validar_crear_ejercicio_descripcion(self):
        response = self.logica.validar_crear_editar_ejercicio("Sentadilla", None, "https://ejercicio.com", 160)
        self.assertEqual(response, "La descripcion es obligatoria")

    def test_validar_crear_ejercicio_enlace(self):
        response = self.logica.validar_crear_editar_ejercicio("Sentadilla", "Lorem ipsum", None, 160)
        self.assertEqual(response, "El link del video es obligatorio")

    def test_validar_crear_ejercicio_calorias(self):
        response = self.logica.validar_crear_editar_ejercicio("Sentadilla", "Lorem ipsum", "https://ejercicio.com", None)
        self.assertEqual(response, "La cantidad de clarias es obligatorio")

    def test_validar_crear_ejercicio_calorias_numerico(self):
        response = self.logica.validar_crear_editar_ejercicio("Sentadilla", "Lorem ipsum", "https://ejercicio.com", "12")
        self.assertEqual(response, "La cantidad de calorias debe ser un valor numerico")