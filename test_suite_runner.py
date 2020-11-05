import unittest

import tests.test_statics as statics
import tests.test_maquina as maquina

# incializar test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# agregar pruebas a la test suite
suite.addTests(loader.loadTestsFromModule(statics))
suite.addTests(loader.loadTestsFromModule(maquina))

# inicializar runner y pasarle la suite
runner = unittest.TextTestRunner()
result = runner.run(suite)