import unittest
import tests.statics as func


class TestStatics(unittest.TestCase):

    def test_is_escalera(self):
        # True si es escalera
        self.assertTrue(func.is_escalera([1, 2, 3, 4, 5, 6]))  # escalera ordenada
        self.assertTrue(func.is_escalera([6, 4, 5, 1, 3, 2]))  # escalera desordenada
        self.assertFalse(func.is_escalera([2, 3, 4, 5, 6, 8]))  # no es escalera, 6 dados
        self.assertFalse(func.is_escalera([1, 5, 4]))  # no es escalera, <6 dados
        self.assertFalse(func.is_escalera([1, 2, 3, 4, 5]))  # no es escalera, <6 dados

    def test_hay_triples(self):
        # True si hay triples
        self.assertTrue(func.hay_triples([1, 1, 1, 2, 3]))  # triple <6 dados
        self.assertTrue(func.hay_triples([5, 3, 4, 3, 6, 3]))  # triple 6 dados
        self.assertTrue(func.hay_triples([6, 6, 6]))  # solo triple
        self.assertFalse(func.hay_triples([1, 5, 6, 2, 3, 4]))  # no hay triple 6 dados
        self.assertFalse(func.hay_triples([1, 4, 1, 4]))  # no hay triple <6 dados

    def test_turno_perdido(self):
        # True si pierde el turno
        self.assertTrue(func.turno_perdido([2, 6, 4, 3, 2, 4]))  # perdido 6 dados
        self.assertTrue(func.turno_perdido([4, 6, 2, 2]))  # perdido <6 dados
        self.assertFalse(func.turno_perdido([4, 3, 6, 2, 1, 6]))  # no perdido 6 dados (1)
        self.assertFalse(func.turno_perdido([4, 5, 6, 2, 3, 6]))  # no perdido 6 dados (5)
        self.assertFalse(func.turno_perdido([1, 6, 4, 2]))  # no perdido <6 dados (1)
        self.assertFalse(func.turno_perdido([4, 6, 5, 2]))  # no perdido <6 dados (5)
        self.assertFalse(func.turno_perdido([4, 1, 5, 2]))  # no perdido <6 dados (1 y 5)
        self.assertFalse(func.turno_perdido([2, 6, 2, 2]))  # no perdido <6 dados (triple)
        self.assertFalse(func.turno_perdido([6, 2, 3, 6, 4, 6]))  # no perdido 6 dados (triple)

    def test_calcular_puntos(self):
        self.assertEqual(func.calcular_puntos([1, 5]), 150)
        self.assertEqual(func.calcular_puntos([6, 6, 6]), 600)
        self.assertEqual(func.calcular_puntos([2, 2, 2, 1, 5]), 350)
        self.assertEqual(func.calcular_puntos([2, 3, 4, 6, 2, 4]), 0)
        self.assertNotEqual(func.calcular_puntos([5, 5, 5, 1]), 250)
        self.assertNotEqual(func.calcular_puntos([1, 1, 1, 5, 5, 5]), 450)

    def test_maquina_hay_triples(self):
        # 0 si no hay triples, sino num triple
        self.assertEqual(func.maquina_hay_triples([1, 1, 1, 5, 6, 2]), 1)
        self.assertEqual(func.maquina_hay_triples([6, 4, 6, 6]), 6)
        self.assertEqual(func.maquina_hay_triples([1, 2, 3, 4, 5]), 0)
        self.assertNotEqual(func.maquina_hay_triples([5, 5, 5]), 0)

if __name__ == '__main__':
    unittest.main()