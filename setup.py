from setuptools import setup
from os import path
from figa import __VERSION__ as VERSION

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.rst"), "r") as readme:
    long_desc = readme.read()

setup(
    name="figa",
    description="Python library designed to handle project configuration on multiple environments.",
    long_description=long_desc,
    version=VERSION,
)
