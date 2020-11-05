import unittest
import tests.maquina as func

class TestMaquina(unittest.TestCase):
    def setUp(self):
        self.maqC = func.MaquinaConservador("Conservador")
        self.maqN = func.MaquinaNormal("Normal")
        self.maqA = func.MaquinaAgresivo("Agresivo")
        self.jug = func.Jugador("Persona")

    def test_init(self):
        self.assertIsInstance(self.maqC, func.Jugador)  # hereda atributos
        self.assertIsInstance(self.maqN, func.MaquinaConservador)  # heredan metodo elegir de conservador
        self.assertIsInstance(self.maqA, func.MaquinaConservador)
        self.assertNotIsInstance(self.jug, func.MaquinaAgresivo)

        self.assertEqual(self.maqC.nombre, "Conservador")
        self.assertEqual(self.maqN.puntosTotal, 0)

    def test_elegir(self):
        # recibe numeros, devuelve lista con indices
        self.assertEqual(self.maqC.elegir([1, 2, 5, 3, 4]), [0, 2])
        self.assertEqual(self.maqA.elegir([1, 1, 5, 4, 1]), [0, 1, 2, 4])
        self.assertEqual(self.maqN.elegir([4, 3, 2, 6]), [])

    def test_seguir(self):
        # recibe puntos, devuelve True o False
        self.assertTrue(self.maqC.seguir(50))
        self.assertFalse(self.maqN.seguir(300))
        self.assertTrue(self.maqA.seguir(250))

if __name__ == "__main__":
    unittest.main()