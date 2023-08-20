from argparse import ArgumentParser
from pathlib import Path

from split_gpx import split_gpx


def main():
    parser = ArgumentParser(description="Split GPX track")
    parser.add_argument("source_path", type=str, help="The GPX file to split.")
    parser.add_argument(
        "target_directory",
        type=str,
        help="The target directory to write the segments to.",
    )
    parser.add_argument(
        "-p",
        "--points",
        type=int,
        dest="points",
        default=500,
        help="Maximum number of points per track (default: %(default)s).",
    )

    arguments = parser.parse_args()

    split_gpx(
        source_path=Path(arguments.source_path),
        target_directory=Path(arguments.target_directory),
        max_segment_points=arguments.points,
    )


if __name__ == "__main__":
    main()
