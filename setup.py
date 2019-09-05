#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name="praetor",
    version="0.1",
    description="Praetor: Web UI for Prefect",
    author="Mikhail Akimov",
    author_email="rovinj.akimov@gmail.com",
    url="https://github.com/roveo/praetor",
    packages=find_packages(),
    scripts=["praetor/bin/praetor"],
    install_requires=[
        "requests",
        "requests-toolbelt",
        "prefect @ git+https://github.com/prefecthq/prefect.git",
        "pydantic"
        # "prefect",
    ],
    extras_require={
        "webserver": [
            "sqlalchemy",
            "psycopg2-binary",
            "starlette",
            "fastapi",
            "uvicorn",
            "pydantic",
            "aiofiles",
        ],
        "dev": [
            "alembic",
            "pytest",
            "pytest-pep8",
            "pytest-cov",
            "black",
            "pylint",
            "coverage",
        ],
    },
)
