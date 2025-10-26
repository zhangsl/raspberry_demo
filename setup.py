from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="raspberry-pi-demo",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A collection of Raspberry Pi demo projects with sensor detection and email alerts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/raspberry-pi-demo",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Home Automation",
        "Topic :: Software Development :: Embedded Systems",
    ],
    python_requires=">=3.7",
    install_requires=[
        "RPi.GPIO",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
        ],
    },
)