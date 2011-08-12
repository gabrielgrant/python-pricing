from setuptools import setup

setup(
    name='python-pricing',
    version='0.1.0dev',
    author='Gabriel Grant',
    packages=['pricing',],
    license='LGPL',
    long_description=open('README').read(),
    install_requires=[
        'python-dsl-tools',
        'unittest2',
        'mock',
    ],
    dependency_links = [
    	'http://github.com/gabrielgrant/python-dsl-tools/tarball/master#egg=python-dsl-tools',
    ]
)

