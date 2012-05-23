from distutils.core import setup

setup(
    name='PyVinil',
    version='0.1.0',
    author='Igor Bonadio',
    author_email='igorbonadio@gmail.com',
    packages=['pyvinil', 'pyvinil.test'],
    url='https://github.com/igorbonadio/pyvinil',
    license='LICENSE.txt',
    description='PyVinil is a Python library, which uses Vinil (a C library), for creating, reading and writing virtual hard disks.',
    long_description=open('README.txt').read(),
)