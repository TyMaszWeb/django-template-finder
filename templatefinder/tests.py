import unittest
import sys


class TestTemplateFinder(unittest.TestCase):

    def test_dummy(self):
        self.fail('Foo bar')


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTemplateFinder)
    unittest.TextTestRunner().run(suite)
    sys.exit()
