from unittest import TestLoader, TextTestRunner

suite = TestLoader().discover('.', 'test_*.py')

TextTestRunner(verbosity=2).run(suite)
