import unittest
from datetime import datetime, time

from src.logica.logica_service import LogicaService
from src.modelo.declarative_base import create_context
from src.modelo.persona import Persona
from src.modelo.ejercicio import Ejercicio
from src.modelo.entrenamiento import Entrenamiento
import random
from faker import Faker



class LogicaServiceTestCase(unittest.TestCase):

    def setUp(self):
        engine, base, session = create_context(True)
        self.logica = LogicaService(engine, base, session)

        # Creacion datos de prueba
        self.session = session

        self.data_factory = Faker("es_CO")

        Faker.seed(1000)
        self.personas_mock = []
        self.ejercicio_mock = []
        self.entrenamiento_mock = []
        nombre_ejercicios = [
            "Sentadillas",
            "Press de banca",
            "Peso muerto",
            "Dominadas",
            "Fondos en paralelas",
            "Remo con barra",
            "Press militar",
            "Zancadas",
            "Curl de bíceps",
            "Elevaciones laterales"
        ]

        #Creamos los datos fake
        for i in range(0,10):
            persona = Persona(nombre=self.data_factory.name(),
                              apellidos=self.data_factory.last_name(),
                              fecha_inicio=self.data_factory.date_time(),
                              talla=self.data_factory.random_int(min=140,max=200),
                              peso=self.data_factory.random_int(min=45,max=150),
                              edad=self.data_factory.random_int(min=15,max=90),
                              medida_brazo=self.data_factory.random_int(min=50,max=170),
                              medida_pecho=self.data_factory.random_int(min=40,max=90),
                              medida_cintura=self.data_factory.random_int(min=40,max=120),
                              medida_pierna=self.data_factory.random_int(min=50,max=120),
                              medida_abdomen=self.data_factory.random_int(min=30,max=90)
                              )
            self.personas_mock.append(persona)
            self.session.add(persona)

            ejercicio = Ejercicio(nombre=nombre_ejercicios[i],
                                  descripcion=self.data_factory.text(),
                                  calorias=self.data_factory.random_int(min=10,max=600),
                                  enlace_video=self.data_factory.url()
                                  )
            self.ejercicio_mock.append(ejercicio)
            self.session.add(ejercicio)

            custom_date = self.data_factory.date_between(start_date="-5y",end_date="today")

            entrenamiento = Entrenamiento(fecha=datetime(custom_date.year, custom_date.month, custom_date.day),
                                          cat_repeticiones=self.data_factory.random_int(min=3,max=15),
                                          tiempo=time(hour=self.data_factory.random_int(min=0,max=2), minute=self.data_factory.random_int(min=0,max=59), second=self.data_factory.random_int(min=0,max=59))
                                          )
            self.entrenamiento_mock.append(entrenamiento)
            self.session.add(entrenamiento)

        for persona, entrenamiento in zip(self.personas_mock, self.entrenamiento_mock):
            persona.entrenamientos = [entrenamiento]

        #Relacionamos los datos
        for ejercicio, entrenamiento in zip(self.ejercicio_mock, self.entrenamiento_mock):
            ejercicio.entrenamientos = [entrenamiento]


        self.session.commit()


    def tearDown(self):
        self.session.query(Entrenamiento).delete()
        self.session.query(Ejercicio).delete()
        self.session.query(Persona).delete()
        self.session.commit()
        self.session.close()
        self.personas_mock = []
        self.ejercicio_mock = []
        self.entrenamiento_mock = []
        self.logica = None

    def test_dar_personas_listado(self):
        personas = self.logica.dar_personas()
        self.assertIsInstance(personas, list)

    def test_dar_personas_organizado(self):
        personas = self.logica.dar_personas()
        self.assertEqual(personas, sorted(personas, key=lambda p: p.nombre))

    def test_dar_entrenamientos_listado(self):
        persona_id = self.personas_mock[-1].id
        entrenamientos = self.logica.dar_entrenamientos(persona_id)
        self.assertIsInstance(entrenamientos, list)


    def test_regresar_entrenamientos(self):
        persona_id = self.personas_mock[-1].id
        entrenamientos = self.logica.dar_entrenamientos(persona_id)
        entreno = entrenamientos[0]
        ejercicio_id = entreno.ejercicio
        nombre_ejercicio = self.session.query(Ejercicio).get(ejercicio_id).nombre
        self.assertEqual(nombre_ejercicio, "Elevaciones laterales")

    def test_comprobar_asociacion_entrenamientos(self):
        entrenamientos = self.logica.dar_entrenamientos(1)
        self.assertTrue(all(ent.persona == 1 for ent in entrenamientos))

    def test_dar_entrenamientos_organizado(self):
        entrenamientos = self.logica.dar_entrenamientos(1)
        self.assertEqual(entrenamientos, sorted(entrenamientos, key=lambda p: p.fecha))

    def test_crear_entrenamientos_sin_asignacion(self):
        with self.assertRaises(ValueError) as context:
            self.logica.crear_entrenamiento(None, None, datetime(2025, 2, 20), 12, time(hour=0, minute=10, second=2))

        self.assertEqual(str(context.exception), "El entrenamiento no puede ser generado")

    def test_asignacion_entrenamientos(self):
        persona1 = self.session.query(Persona).get(1)
        ejercicio1 = self.session.query(Ejercicio).get(1)
        self.logica.crear_entrenamiento(persona1, ejercicio1, datetime(2025, 2, 20), 12,
                                        time(hour=0, minute=10, second=2))
        entrenamientos_asignados = self.session.query(Entrenamiento).order_by(Entrenamiento.id.desc()).first()
        self.assertEqual(entrenamientos_asignados.persona, 1)
        self.assertEqual(entrenamientos_asignados.ejercicio, 1)

    def test_validacion_formato_tiempo(self):
        persona1 = self.session.query(Persona).get(1)
        ejercicio1 = self.session.query(Ejercicio).get(1)
        with self.assertRaises(ValueError) as context:
            self.logica.crear_entrenamiento(persona1, ejercicio1, datetime(2025, 2, 20), 12, None)

        self.assertEqual(str(context.exception), "El formato de tiempo no es el correcto")

    def test_validar_crear_ejercicio(self):
        try:
            self.logica.validar_crear_editar_ejercicio("Sentadilla", "Lorem ipsum", "https://ejercicio.com", "160")
        except ValueError as context:
            self.fail(f"Error en el metodo validar_crear_editar_ejercicio: {context}")

    def test_validar_crear_ejercicio_nombre(self):
        response = self.logica.validar_crear_editar_ejercicio(None, "Lorem ipsum", "https://ejercicio.com", "160")
        self.assertEqual(response, "El nombre es obligatorio")

    def test_validar_crear_ejercicio_descripcion(self):
        response = self.logica.validar_crear_editar_ejercicio("Sentadilla", None, "https://ejercicio.com", "160")
        self.assertEqual(response, "La descripcion es obligatoria")

    def test_validar_crear_ejercicio_enlace(self):
        response = self.logica.validar_crear_editar_ejercicio("Sentadilla", "Lorem ipsum", None, "160")
        self.assertEqual(response, "El link del video es obligatorio")

    def test_validar_crear_ejercicio_calorias(self):
        response = self.logica.validar_crear_editar_ejercicio("Sentadilla", "Lorem ipsum", "https://ejercicio.com",
                                                              None)
        self.assertEqual(response, "La cantidad de calorias es obligatorio")

    def test_validar_crear_ejercicio_calorias_numerico(self):
        response = self.logica.validar_crear_editar_ejercicio("Sentadilla", "Lorem ipsum", "https://ejercicio.com",
                                                              "Lorem ipsum")
        self.assertEqual(response, "La cantidad de calorias debe ser un valor numerico")

    def test_validar_crear_ejercicio_exitoso(self):
        response = self.logica.validar_crear_editar_ejercicio("Sentadilla", "Lorem ipsum", "https://ejercicio.com",
                                                              "12")
        self.assertEqual(response, "")

    def test_crear_ejercicio(self):
        try:
            self.logica.crear_ejercicio("Sentadilla", "Lorem ipsum", "https://ejercicio.com", "160")
        except ValueError as context:
            self.fail(f"Error en el metodo crear_ejercicio: {context}")

    def test_crear_ejercicio_verificar_almacenamiento(self):
        self.logica.crear_ejercicio("Sentadilla_Test", "Lorem ipsum", "https://ejercicio.com", "160")
        serch_ejercicio = self.session.query(Ejercicio).filter(Ejercicio.nombre == "Sentadilla_Test").first()
        self.assertNotEqual(serch_ejercicio, None)
