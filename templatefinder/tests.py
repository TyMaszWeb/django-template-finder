from django.conf import settings
from django.utils import unittest

from . import find_all_templates, flatten_template_loaders, template_choices


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


class DisplayNamesTests(unittest.TestCase):
    """
    Various scenarios involving the template_choices utility function.
    """
    def setUp(self):
        settings.TEMPLATE_LOADERS = (
            'django.template.loaders.app_directories.Loader',
        )
        settings.TEMPLATEFINDER_DISPLAY_NAMES = {
            'menu/menu.html': 'Global menu',
            'menu/submenu.html': 'Global Sub-menu',
            'menu/complicated_file-name.20xx.html': 'We keep hyphens!',
        }

    def test_calculating_fallback_names(self):
        """
        Without any setting, the filename of each template in the found
        template paths should be used to calculate a human-friendly version.
        """
        templates = find_all_templates('menu/*')
        # note: we pass in an empty dictionary, because we can't use
        # the override_settings() decorator or the settings() context manager
        # and expect tests to pass in 1.3
        template_tuple = template_choices(templates=templates,
                                          display_names={})
        self.assertEqual(list(template_tuple), [
            (u'menu/complicated_file-name.20xx.html', u'Complicated file-name 20xx'),
            (u'menu/menu.html', u'Menu'),
            (u'menu/submenu.html', u'Submenu')
        ])

    def test_calculating_usage_provided_names(self):
        """
        Given a dictionary of template->title mappings on a per-usage basis,
        prefer the provided ones over either the fallbacks or the global
        setting, even if provided.
        """
        templates = find_all_templates('menu/*')
        template_tuple = template_choices(templates=templates,
                                          display_names={
                                              'menu/menu.html': 'Main Menu',
                                              'menu/nonexistant.html': 'Fail',
                                          })
        self.assertEqual(list(template_tuple), [
            (u'menu/complicated_file-name.20xx.html', u'Complicated file-name 20xx'),
            (u'menu/menu.html', u'Main Menu'),
            (u'menu/submenu.html', u'Submenu')
        ])

    def test_calculating_global_provided_names(self):
        """
        If no display name mapping is provided, and the global setting is
        defined, prefer it to the fallback calculated names.
        """
        templates = find_all_templates('menu/*')
        template_tuple = template_choices(templates=templates,
                                          display_names=None)
        self.assertEqual(list(template_tuple), [
            (u'menu/complicated_file-name.20xx.html', u'We keep hyphens!'),
            (u'menu/menu.html', u'Global menu'),
            (u'menu/submenu.html', u'Global Sub-menu')
        ])
