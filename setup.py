from setuptools import setup, find_packages

version = None

with open('version.txt') as version_file:
    version = version_file.read().strip()

setup(
    name="tandora-payanpaadu",
    version=version,
    packages=find_packages(exclude=["tandorautils", "*.txt", ])
)
