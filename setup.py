from setuptools import setup, find_packages

setup(
    name="colorfilters",
    version="1.0.0",
    author="Alexander Reynolds",
    install_requires=["opencv-python"],
    packages=find_packages(),
    description="Image thresholding in multiple colorspaces.",
)
