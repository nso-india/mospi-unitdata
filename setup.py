from setuptools import setup, find_packages

setup(
    name="MospiUnitdata",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="DIID,Ministry of Statistics and Programme Implementation",
    description="This package can be used to download the data from MoSPI Microdata " \
    "Portal (https://microdata.gov.in). Kindly call the getDatasets method with First parameter as location to save the data and second Parameter as " \
    "API key generated from MicroData Portal Profile Section.",
)