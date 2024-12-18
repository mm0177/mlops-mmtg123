from setuptools import find_packages, setup

with open("requirements.txt", "r") as file:
    requirements = file.read().splitlines()

setup(
    name="mlops",
    version="0.0.1",
    author="meyyappan",
    author_email="",
    install_requires=requirements,
    packages=find_packages(),
)
