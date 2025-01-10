from setuptools import setup, find_packages

setup(
    name="vortex",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pytest>=7.0.0",
        "coincurve>=18.0.0",
        "base58>=2.1.0",
        "mnemonic>=0.20",
        "cryptography>=3.4.7",
    ],
    python_requires=">=3.8",
) 