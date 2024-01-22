from setuptools import find_packages, setup
setup(
    name='macti',
    packages=find_packages(include=['macti', 'macti.fdm', 'macti.PyNoxtli']),
    include_package_data=True,
    package_data={'':['data/resources/*', 'data/resources/.nbgex']},
    version='2.0',
    description='Macti Lib',
    author='Luis M. de la Cruz',
    license='CC',
)
