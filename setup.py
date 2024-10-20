from setuptools import setup, find_packages

setup(
    name="rodeo",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "requests",
        "openai",
        # other dependencies...
    ],
    entry_points={
        "console_scripts": [
            "rodeo=rodeo.cli:main",
        ],
    },
)
