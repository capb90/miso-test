import unittest

from src.logica.LogicaMock import LogicaMock

class LogicaMockTestCase(unittest.TestCase):

    def setUp(self):
        self.logica = LogicaMock()
        
    def tearDown(self):
        self.logica = None
        
    def test_dar_persona(self):
        persona = self.logica.dar_persona(1)
        self.assertEqual(persona["nombre"], "Angelica")
        self.assertEqual(persona["apellido"], "Mora")

    def test_dar_persona_error(self):
        persona = self.logica.dar_persona(1)
        self.assertEqual(persona["apellido"], "Mora")
