from setuptools import setup, find_packages

setup(
    name="networking-labs-cli",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["boto3", "botocore"],
    entry_points={
        "console_scripts": ["nmcli=main:main"]
    },
)
