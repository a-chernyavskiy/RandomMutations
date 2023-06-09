import os
from setuptools import setup


def read(filename: str):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name="randmut",
    version="0.1",
    author="Andrey Chernyavskiy",
    author_email="andrey.chernyavskiy@gmail.com",
    description="Random mutations global optimization algorithm",
    license="GPL-3.0",
    keywords="optimization, global optimization, evolutionary algorithms",
    url="https://github.com/a-chernyavskiy/randmut",
    packages=["randmut"],
    long_description=read("README.md"),
    install_requires=["numpy", "pytest"]
)