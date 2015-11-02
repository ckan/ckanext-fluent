from setuptools import setup, find_packages
import sys, os

version = '1.0.0'

setup(
    name='ckanext-fluent',
    version=version,
    description="Multilingual fields for CKAN",
    long_description="""
    """,
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Government of Canada',
    author_email='ian@excess.org',
    url='',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points=\
    """
    [ckan.plugins]
    fluent=ckanext.fluent.plugins:FluentPlugin
    """,
)
