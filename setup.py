# Copyright (C) 2020 Clement Demonchy
from setuptools import setup
import sys
import os

assert sys.version_info >= (3, 6, 0), "ftg requires Python 3.6+"
from pathlib import Path

CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))  # for setuptools.build_meta


def get_long_description() -> str:
    return (
        (CURRENT_DIR / "README.md").read_text(encoding="utf8")
    )

setup(
    name="ftg",
    description="Random table generator",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Clement Demonchy",
    url="https://github.com/knil-sama/fake-table-generator",
    license="Apache",
    packages=["fake_table_generator"],
    package_dir={"": "src"},
    python_requires=">=3.6",
    zip_safe=False,
    install_requires=[
        "faker",
        "psycopg2-binary",
        "tqdm",
        "typing",
        "click>=7.1.2",
    ],
    extras_require={
        #"d": ["aiohttp>=3.3.2", "aiohttp-cors"],
    },
    test_suite="tests.test_black",
    classifiers=[
        "Development Status :: Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    entry_points={
        "console_scripts": [
            "black=black:patched_main",
        ]
    },
)
