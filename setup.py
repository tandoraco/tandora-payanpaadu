from setuptools import setup, find_packages

setup(
    name="tandora-payanpaadu",
    version="1.0",
    packages=find_packages(exclude=["tandorautils", ])
)
