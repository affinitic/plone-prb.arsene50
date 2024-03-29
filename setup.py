# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = \
    read('README.rst') + \
    read('CHANGES.txt')

setup(
    name='prb.arsene50',
    version='0.1.9.dev0',
    description="view events from arsene 50",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='Python Plone PRB CIRB BRIC',
    author='Benoît Suttor',
    author_email='bsuttor@cirb.irisnet.be',
    url='http://pypi.python.org/pypi/prb.arsene50',
    license='BSD',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['prb'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Plone',
        'setuptools',
        'plone.api',
        'Products.LinguaPlone',
        'requests',
        'plone.memoize',
    ],
    extras_require={
        'test': [
            'plone.app.robotframework',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
