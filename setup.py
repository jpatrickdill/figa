from setuptools import setup, find_packages
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
    url="https://github.com/jpatrickdill/figa",
    author="Patrick Dill <jamespatrickdill@gmail.com>",
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords="config, ini, cfg, configure",
    packages=find_packages(),
    python_requires='>=3.0, <4',

    install_requires=["pyyaml", "configobj", "toml", "pyhocon"]
)
