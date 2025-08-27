from setuptools import setup, find_packages

setup(
    name="assets",
    version="0.1.0",
    description="Python package for modeling financial instruments such as stocks, forex, futures, and options.",
    author="AZ",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",  
    ],
    extras_require={
        "price_providers": ["yfinance"]
    },
    python_requires=">=3.8",
)
