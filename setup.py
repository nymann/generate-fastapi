import setuptools
from distutils import util

version = dict()
path = util.convert_path("src/generate_fastapi/version.py")
with open(path) as file:
    exec(file.read(), version)

setuptools.setup(version=version["__version__"])
