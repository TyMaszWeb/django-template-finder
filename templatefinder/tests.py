from django.conf import settings
from django.utils import unittest

from . import find_all_templates


class TemplateFinderTestMixin(object):

    def test_explicit_name(self):
        self.assertEqual(['404.html'], find_all_templates('404.html'))

    def test_wildcard_name(self):
        self.assertIn('403.html', find_all_templates('40*.html'))
        self.assertIn('404.html', find_all_templates('40*.html'))

    def test_subdirectory_wildcard(self):
        self.assertIn('menu/menu.html', find_all_templates('menu/*'))
        self.assertIn('menu/submenu.html', find_all_templates('menu/*'))


class AppDirectoriesLoaderTest(TemplateFinderTestMixin, unittest.TestCase):

    def setUp(self):
        settings.TEMPLATE_LOADERS = (
            'django.template.loaders.app_directories.Loader',
        )


class CachedLoaderTest(TemplateFinderTestMixin, unittest.TestCase):

    def setUp(self):
        settings.TEMPLATE_LOADERS = (
            'django.template.loaders.cached.Loader', (
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            )
        )


class FilesystemLoaderTest(TemplateFinderTestMixin, unittest.TestCase):

    def setUp(self):
        settings.TEMPLATE_LOADERS = (
            'django.template.loaders.filesystem.Loader',
        )
