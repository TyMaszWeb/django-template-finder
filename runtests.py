import os.path
import unittest

import django
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
        ),
        TEMPLATE_DIRS=(
            os.path.join(os.path.dirname(__file__), 'templatefinder', 'test_project', 'templates'),
        )
    )
    if hasattr(django, 'setup'):
        django.setup()
    suite = unittest.TestLoader().loadTestsFromModule(tests)
    return suite
