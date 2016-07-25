import sys

from setuptools import find_packages, setup


with open('README.rst') as f:
    long_description = f.read()

install_requires = [
    'PyYAML >=3.11, <4',
    'sr.comp.ranker >=1.0, <2',
    'mock >=1.0.1, <2',
    'python-dateutil >=2.2, <3'
]

if sys.version_info < (3, 4):
    install_requires.append('enum34 >=1.0.4, <2')

setup(
    name='sr.comp',
    version='1.1.0',
    packages=find_packages(),
    namespace_packages=['sr', 'sr.comp'],
    description='Student Robotics Competition Software',
    long_description=long_description,
    author='Student Robotics Competition Software SIG',
    author_email='srobo-devel@googlegroups.com',
    install_requires=install_requires,
    setup_requires=[
        'nose >=1.3, <2',
        'Sphinx >=1.3, <2'
    ],
    test_suite='nose.collector'
)
