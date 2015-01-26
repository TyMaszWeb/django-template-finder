import fnmatch
import logging
import os

from django.conf import settings


try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module

try:
    from django.utils.six import string_types
except ImportError:
    string_types = (basestring,)
try:
    from django.template import Engine
except ImportError:
    class Engine(object):
        @staticmethod
        def get_default():
            return None

__all__ = ('find_all_templates', 'flatten_template_loaders')


LOGGER = logging.getLogger('templatefinder')


def flatten_template_loaders(templates):
    """
    Given a collection of template loaders, unwrap them into one flat iterable.

    :param templates: template loaders to unwrap
    :return: template loaders as an iterable of strings.
    :rtype: generator expression
    """
    for loader in templates:
        if not isinstance(loader, string_types):
            for subloader in flatten_template_loaders(loader):
                yield subloader
        else:
            yield loader


def find_all_templates(pattern='*.html'):
    """
    Finds all Django templates matching given glob in all TEMPLATE_LOADERS

    :param str pattern: `glob <http://docs.python.org/2/library/glob.html>`_
                        to match

    .. important:: At the moment egg loader is not supported.
    """
    templates = []
    template_loaders = flatten_template_loaders(settings.TEMPLATE_LOADERS)
    for loader_name in template_loaders:
        module, klass = loader_name.rsplit('.', 1)
        if loader_name in (
            'django.template.loaders.app_directories.Loader',
            'django.template.loaders.filesystem.Loader',
        ):
            loader_class = getattr(import_module(module), klass)
            if getattr(loader_class, '_accepts_engine_in_init', False):
                loader = loader_class(Engine.get_default())
            else:
                loader = loader_class()
            for dir in loader.get_template_sources(''):
                for root, dirnames, filenames in os.walk(dir):
                    for basename in filenames:
                        filename = os.path.join(root, basename)
                        rel_filename = filename[len(dir)+1:]
                        if fnmatch.fnmatch(filename, pattern) or \
                           fnmatch.fnmatch(basename, pattern) or \
                           fnmatch.fnmatch(rel_filename, pattern):
                            templates.append(rel_filename)
        else:
            LOGGER.debug('%s is not supported' % loader_name)
    return sorted(set(templates))
