from unittest import TestLoader, TextTestRunner

suite = TestLoader().discover('.', 'test_*.py')

TextTestRunner().run(suite)
