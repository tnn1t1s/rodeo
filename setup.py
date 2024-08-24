from setuptools import setup, find_packages

setup(
    name="rodeo-cli",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "rodeo-cli=rodeo.main:main",
        ],
    },
)
