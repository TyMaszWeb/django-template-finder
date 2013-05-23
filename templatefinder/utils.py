import fnmatch
import logging
import os

from django.conf import settings
from django.utils.importlib import import_module


__all__ = ('find_all_templates',)


LOGGER = logging.getLogger('templatefinder')


def find_all_templates(pattern='*.html'):
    """
    Finds all Django templates matching given glob in all TEMPLATE_LOADERS

    :param str pattern: `glob <http://docs.python.org/2/library/glob.html>`_
                        to match

    .. important:: At the moment egg loader is not supported.
    """
    templates = []

    # See: https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
    template_loaders = list(settings.TEMPLATE_LOADERS)
    if 'django.template.loaders.cached.Loader' in template_loaders:
        cached_loader_index = template_loaders.index('django.template.loaders.cached.Loader')
        extra_loaders = template_loaders[cached_loader_index + 1]
        # both the cached loader and the next element (list of regular loaders)
        del template_loaders[cached_loader_index]
        del template_loaders[cached_loader_index]
        for loader in extra_loaders:
            template_loaders.insert(cached_loader_index, loader)

    for loader_name in template_loaders:
        module, klass = loader_name.rsplit('.', 1)
        if loader_name in (
            'django.template.loaders.app_directories.Loader',
            'django.template.loaders.filesystem.Loader',
        ):
            loader = getattr(import_module(module), klass)()
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
