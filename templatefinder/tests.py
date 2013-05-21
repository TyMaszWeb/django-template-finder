import unittest


class TestTemplateFinder(unittest.TestCase):

    def test_dummy(self):
        self.fail('Make it real mate')


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTemplateFinder)
    return suite
