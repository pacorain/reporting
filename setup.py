from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read()

setup(
    name='Austin Rainwater Reporting',
    version='0.0.1',
    packages=['reporting'],
    install_requires=requirements
)
