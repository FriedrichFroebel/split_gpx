# GPX splitter

Simple tool to split a GPX file into multiple parts.

## Features

At the moment, this only supports splitting GPX files after a fixed number of track points.

I mostly wrote this module for myself to make it easier to install it as I commonly need this functionality to successfully send full tracks to my GPS device which only supports 500 points per track.

## Installation

You can install this package from PyPI:

```bash
python -m pip install split_gpx
```

Alternatively, you can use the package from source directly after installing the required dependencies.

## Usage

To see the supported CLI parameters, just run:

```bash
python -m split_gpx --help  # or `split_gpx --help`
```

## License

This package is subject to the terms of the MIT license.
