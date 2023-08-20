from pathlib import Path

import setuptools


ROOT_DIRECTORY = Path(__file__).parent.resolve()


setuptools.setup(
    name="split_gpx",
    description="Split a GPX tracks into multiple parts",
    version="0.1.0",
    license="MIT",
    long_description=Path(ROOT_DIRECTORY / "README.md").read_text(encoding="UTF-8"),
    long_description_content_type="text/markdown",
    author="FriedrichFröbel",
    url="https://github.com/FriedrichFroebel/split_gpx",
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.8, <4",
    install_requires=[
        "gpxpy",
    ],
    extras_require={
        "dev": [
            "black",
            "flake8",
            "pep8-naming",
            "mypy",
        ]
    },
    entry_points={
        "console_scripts": [
            "split_gpx=split_gpx.__main__:main",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    keywords=["gps", "gpx", "track"],
)
