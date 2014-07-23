from django.conf import settings
from django.utils import unittest

from . import find_all_templates, flatten_template_loaders


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
            ('django.template.loaders.cached.Loader', (
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            )),
        )


class FilesystemLoaderTest(TemplateFinderTestMixin, unittest.TestCase):

    def setUp(self):
        settings.TEMPLATE_LOADERS = (
            'django.template.loaders.filesystem.Loader',
        )


class FlatteningTemplateLoaders(unittest.TestCase):
    def test_standard_template_loaders(self):
        TEMPLATE_LOADERS = (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )
        expected = list(TEMPLATE_LOADERS)
        received = list(flatten_template_loaders(TEMPLATE_LOADERS))
        self.assertEqual(expected, received)

    def test_loaders_nested_under_caching_loader(self):
        TEMPLATE_LOADERS = (
            ('django.template.loaders.cached.Loader', (
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            )),
        )
        expected = [
            'django.template.loaders.cached.Loader',
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]
        received = list(flatten_template_loaders(TEMPLATE_LOADERS))
        self.assertEqual(expected, received)

    def test_bad_caching_configuration(self):
        TEMPLATE_LOADERS = (
            'django.template.loaders.cached.Loader', (
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ),
        )
        expected = [
            'django.template.loaders.cached.Loader',
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]
        received = list(flatten_template_loaders(TEMPLATE_LOADERS))
        self.assertEqual(expected, received)

    def test_loaders_nested_under_anything_else(self):
        TEMPLATE_LOADERS = (
            ('fictional.other_caching.Loader', (
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            )),
        )
        expected = [
            'fictional.other_caching.Loader',
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]
        received = list(flatten_template_loaders(TEMPLATE_LOADERS))
        self.assertEqual(expected, received)

    def test_complex_loader_configuration(self):
        TEMPLATE_LOADERS = (
            ('fictional.other_caching.Loader', (
                'django.template.loaders.filesystem.Loader',
            )),
            ('django.template.loaders.cached.Loader', (
                'django.template.loaders.app_directories.Loader',
            )),
            'django.template.loaders.egg.Loader',
        )
        expected = [
            'fictional.other_caching.Loader',
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.cached.Loader',
            'django.template.loaders.app_directories.Loader',
            'django.template.loaders.egg.Loader',
        ]
        received = list(flatten_template_loaders(TEMPLATE_LOADERS))
        self.assertEqual(expected, received)

