from setuptools import setup, find_packages

version = None

try:
    with open('version.txt') as version_file:
        version = version_file.read().strip()
except Exception:
        version = '2.1.2'

setup(
    name="tandora-payanpaadu",
    version=version,
    packages=find_packages(exclude=["tandorautils", 'karuvi', ])
)
