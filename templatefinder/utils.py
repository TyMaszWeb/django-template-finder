from __future__ import absolute_import

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

    .. important:: At the moment cached loader and egg loader are not supported.
    """
    templates = []
    for loader_name in settings.TEMPLATE_LOADERS:
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
                        if fnmatch.fnmatch(filename, '*' + pattern):
                            templates.append(filename[len(dir)+1:])
        else:
            LOGGER.debug('%s is not supported' % loader)
    return sorted(templates)
