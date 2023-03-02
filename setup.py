from setuptools import setup, find_packages

setup(
    name='mmai',
    version=open('mmai/VERSION').read().strip(),
    description='MMAI helper functions and classes',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=find_packages(),
    include_package_data=True,
)