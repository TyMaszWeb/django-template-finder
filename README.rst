======================
django-template-finder
======================

.. image:: https://api.travis-ci.org/TyMaszWeb/django-template-finder.png?branch=master

django-template-finder is a simple Django utility that allows you to find
templates with names matching given pattern.

Suppose you are writing an app and want to allow your user to choose one of
predefined templates, but don't want to hardcode their names in any way. Scan
for files? What if they are not store in the same directory? This is where
django-template-finder can help you!

Supported template loaders:

- ``django.template.loaders.app_directories.Loader``
- ``django.template.loaders.filesystem.Loader``
- ``django.template.loaders.cached.Loader``

Contributions and comments are welcome using Github at:
http://github.com/TyMaszWeb/django-template-finder

Installation
============

#. `pip install django-template-finder`

That's it! It's just a simple utility library, no need to add anything to
``INSTALLED_APPS``.

You will need a recent version of Django. Chances are django-template-finder
will work with Django 1.2+, however only versions above 1.3 are supported.

Usage
=====

Search for all ``404.html`` templates, recursively, in all template loaders:

::

    from templatefinder import find_all_templates

    find_all_templates('404.html')

Search for all ``4xx.html`` templates, recursively, in all template loaders:

::

    from templatefinder import find_all_templates

    find_all_templates('4*.html')

Search for all templates under ``menu/``, recursively, in all template loaders:

::

    from templatefinder import find_all_templates

    find_all_templates('menu/*')

Generate nicer, human-friendly names for discovered templates in forms:

::

    from templatefinder import find_all_templates, template_choices
    from django.forms.widgets import Select

    class MyForm(Form):
        def __init__(self, *args, **kwargs):
            super(MyForm, self).__init__(*args, **kwargs)
            found_templates = find_all_templates('menu/*')
            choices = template_choices(templates=found_templates, display_names=None)
            self.fields['myfield'].widget = Select(choices=list(choices))

Providing human-friendly names for discovered templates, overriding the built-in
name calculation:

::

    from templatefinder import find_all_templates, template_choices

    found_templates = find_all_templates('menu/*')
    choices = template_choices(templates=found_templates, display_names={
        'menu/menu.html': 'My super awesome menu',
    })

Using a project-wide setting for overriding the template display names:

::

    from django.conf import settings
    # note: this should be in your Django project's settings module, and is
    # only set here for illustration purposes.
    settings.TEMPLATEFINDER_DISPLAY_NAMES = {
        'menu/menu.html': 'Super menu',
        'menu/another-menu.html': 'Another menu',
    }

    from templatefinder import find_all_templates, template_choices

    found_templates = find_all_templates('menu/*')
    choices = template_choices(found_templates)

Bugs & Contribution
===================

Please use Github to report bugs, feature requests and submit your code:
http://github.com/TyMaszWeb/django-template-finder

:author: Piotr Kilczuk
:date: 2013/03/27
