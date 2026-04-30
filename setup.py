from setuptools import setup, find_packages

setup(
    name="networking-labs-cli",
    version="1.0.0",
    author="Carter",
    author_email="justn.carter9527@yahoo.com",
    url="https://github.com/CartierC/networking-labs-cli",
    packages=find_packages(),
    py_modules=["main"],
    install_requires=["boto3", "botocore"],
    entry_points={
        "console_scripts": ["nmcli=main:main"]
    },
)
