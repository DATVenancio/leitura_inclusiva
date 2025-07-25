#!/usr/bin/env python3
"""
Setup script for the Audiobook Reader application.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    with open(requirements_path, "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="audiobook-reader",
    version="1.0.0",
    description="A Python audiobook reader application with tkinter GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/audiobook-reader",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Players",
        "Topic :: Desktop Environment",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "audiobook-reader=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="audiobook player audio tkinter gui",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/audiobook-reader/issues",
        "Source": "https://github.com/yourusername/audiobook-reader",
        "Documentation": "https://github.com/yourusername/audiobook-reader#readme",
    },
) 