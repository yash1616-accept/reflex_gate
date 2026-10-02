from setuptools import setup, find_packages

setup(
    name="reflexgate-sdk",
    version="0.1.0",
    description="The official Python SDK for ReflexGate - The Enterprise AI Safety Firewall",
    long_description=open("README.md").read() if open("README.md") else "ReflexGate Python SDK",
    long_description_content_type="text/markdown",
    author="Your Name",
    url="https://github.com/yourusername/reflexgate",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "pydantic>=2.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
