from setuptools import find_packages, setup


with open('README.rst') as f:
    long_description = f.read()


setup(
    name='sr.comp.ranker',
    version='1.0.0',
    packages=find_packages(),
    namespace_packages=['sr', 'sr.comp'],
    long_description=long_description,
    author='Student Robotics Competition Software SIG',
    author_email='srobo-devel@googlegroups.com',
    setup_requires=[
        'nose >=1.3, <2',
        'Sphinx >=1.3, <2'
    ],
    test_suite='nose.collector',
    zip_safe=False
)
