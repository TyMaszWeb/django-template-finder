import unittest

from django.conf import settings

from templatefinder import tests


def main():
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        INSTALLED_APPS=(
            'templatefinder.test_project.testapp',
        )
    )
    suite = unittest.TestLoader().loadTestsFromModule(tests)
    return suite
