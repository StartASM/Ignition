from setuptools import setup, find_packages

setup(
    name="ignition",
    version="1.0.0",
    description="The StartASM interpreter and step-through debugger",
    author="Tahsin Ahmed",
    author_email="tahsin4466@g.ucla.edu",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "ignition = ignition.main:main",
        ],
    },
    install_requires=[],
    python_requires=">=3.6",
)
