import importlib.resources as resources
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from split_gpx.split_gpx import (
    get_digits,
    get_filename_template,
    get_name_template,
    split_gpx,
)


class GetDigitsTestCase(TestCase):
    def test_one_digit(self):
        self.assertEqual(1, get_digits(5))

    def test_two_digits(self):
        self.assertEqual(2, get_digits(10))
        self.assertEqual(2, get_digits(99))

    def test_more_digits(self):
        self.assertEqual(101, get_digits(10**100 + 1))


class GetFilenameTemplateTestCase(TestCase):
    def test_get_filename_template(self):
        self.assertEqual(
            "my_track_file_{index:02d}.gpx",
            get_filename_template(
                source_path=Path("/home/user/tracks/my_track_file.gpx"),
                segment_count=20,
            ),
        )


class GetNameTemplateTestCase(TestCase):
    def test_name(self):
        self.assertEqual(
            "{index:02d} - My track",
            get_name_template(original_name="My track", segment_count=20),
        )

    def test_no_name(self):
        self.assertEqual(
            "{index:02d} - (empty)",
            get_name_template(original_name=None, segment_count=20),
        )


class SplitGpxTestCase(TestCase):
    def _run_test(
        self, directory_name: str, input_file_name: str, max_segment_points: int
    ):
        input_file = (
            resources.files(f"tests.examples.{directory_name}") / input_file_name
        )
        with TemporaryDirectory() as output_directory:
            output_path = Path(output_directory)
            with resources.as_file(input_file) as input_path:
                split_gpx(
                    source_path=input_path,
                    target_directory=output_path,
                    max_segment_points=max_segment_points,
                )
            output_file_names = {entry.name for entry in output_path.glob("*")}
            expected_file_names = {
                entry.name
                for entry in resources.files(
                    f"tests.examples.{directory_name}"
                ).iterdir()
            } - {input_file_name}
            self.assertEqual(expected_file_names, output_file_names)

            for expected_path in resources.files(
                f"tests.examples.{directory_name}"
            ).iterdir():
                if expected_path.name == input_file_name:
                    continue
                actual_path = output_path / expected_path.name
                self.assertEqual(
                    expected_path.read_text(),
                    actual_path.read_text(),
                    expected_path.name,
                )

    def test_basic(self):
        self._run_test(
            directory_name="basic",
            input_file_name="my_track.gpx",
            max_segment_points=500,
        )
