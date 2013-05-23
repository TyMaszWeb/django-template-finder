#!/usr/bin/env python

import os
from setuptools import setup, find_packages

import templatefinder


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP',
]

setup(
    author='Piotr Kilczuk',
    author_email='piotr@tymaszweb.pl',
    name='django-template-finder',
    version='.'.join(str(v) for v in templatefinder.VERSION),
    description='Simple Django utility that allows you to find templates with names matching given pattern',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    url='https://github.com/TyMaszWeb/django-template-finder',
    license='BSD License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=[],
    tests_require=[
        'tox>=1.4.3',
    ],
    packages=find_packages(),
    include_package_data=False,
    zip_safe=False,
    test_suite='runtests.main',
)
