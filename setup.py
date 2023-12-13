from setuptools import find_packages, setup
setup(
    name='macti',
    packages=find_packages(),#:include=['macti', 'macti.SistemasLineales', 'macti.MetodoEuler', 'macti.PyNoxtli']),
    include_package_data=True,
    package_data={'':['data/SistemasLineales/*.npy', 'data/MetodoEuler/*.npy', 'data/Derivada/Introduccion/.__ans_*', 'data/Plantillas/*.ipynb']},
    version='2.0',
    description='Macti Lib',
    author='Luis M. de la Cruz',
    license='CC',
)
