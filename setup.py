from setuptools import setup, find_packages

setup(
    name="syncuze",
    version="1.0.0",
    description="Python SDK and FastAPI service for SyncUze Engine",
    author="SyncUze Team",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=2.0",
    ],
    extras_require={
        "server": [
            "fastapi>=0.100.0",
            "uvicorn>=0.22.0",
            "sqlalchemy>=2.0.0",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
