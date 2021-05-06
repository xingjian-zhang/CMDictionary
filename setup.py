from setuptools import setup

NAME = 'cmdict'
VERSION = '1.0'
REQUIRES = [
    "arrow>=1.0.3",
    "beautifulsoup4>=4.9.3",
    "bs4>=0.0.1",
    "certifi>=2020.12.5",
    "click>=7.1.2",
    "colorama>=0.4.4",
    "commonmark>=0.9.1",
    "dataclasses>=0.8",
    "joblib>=1.0.1",
    "Pygments>=2.8.1",
    "python-dateutil>=2.8.1",
    "regex>=2021.3.17",
    "rich>=9.13.0",
    "six>=1.15.0",
    "soupsieve>=2.2.1",
    "tinydb>=4.4.0",
    "tqdm>=4.59.0",
    "typing-extensions>=3.7.4.3",
    "urllib3>=1.26.4"
]
DATA = {"cmdict": ["data/*.txt"]}

setup(name=NAME,
      version=VERSION,
      packages=["cmdict"],
      install_requires=REQUIRES,
      package_data=DATA
      )