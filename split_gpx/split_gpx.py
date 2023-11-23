from __future__ import annotations

from math import log10
from pathlib import Path
from typing import Generator

from gpxpy import parse as parse_gpx
from gpxpy.gpx import GPX, GPXTrack, GPXTrackSegment


def get_digits(value: int) -> int:
    return int(log10(value)) + 1


def get_filename_template(source_path: Path, segment_count: int) -> str:
    width = get_digits(segment_count)
    return f"{source_path.stem}_{{index:0{width}d}}{source_path.suffix}"


def get_name_template(original_name: str | None, segment_count: int) -> str:
    original_name = original_name or "(empty)"
    width = get_digits(segment_count)
    return f"{{index:0{width}d}} - {original_name}"


class SplitGpx:
    def __init__(self) -> None:
        self.output_segments: list[GPXTrackSegment] = []
        self.output_segment: GPXTrackSegment = GPXTrackSegment()
        self.track_names: list[str | None] = []

    def add_segment(self, track: GPXTrack | None) -> None:
        self.output_segments.append(self.output_segment)
        self.output_segment = GPXTrackSegment()
        self.track_names.append(track.name if track else None)

    def get_segment_length(self) -> int:
        return len(self.output_segment.points)

    def generate_segments(self, gpx: GPX, max_segment_points: int) -> None:
        previous_track: GPXTrack | None = None
        for track in gpx.tracks:
            if self.get_segment_length() > 0:
                self.add_segment(track=previous_track)

            for segment in track.segments:
                if self.get_segment_length() > 0:
                    self.add_segment(track=track)
                for point in segment.points:
                    self.output_segment.points.append(point)

                    if self.get_segment_length() >= max_segment_points:
                        self.add_segment(track=track)
                        # Make sure to the segments are connected.
                        self.output_segment.points.append(point)
            previous_track = track
        if self.get_segment_length() > 0:
            self.add_segment(track=track)

    @property
    def segment_count(self) -> int:
        return len(self.output_segments)

    def get_name_templates(self) -> dict[str | None, str]:
        return {
            name: get_name_template(name, self.track_names.count(name))
            for name in set(self.track_names)
        }

    def get_enumerated_segments(
        self,
    ) -> Generator[tuple[int, GPXTrackSegment, str | None], None, None]:
        for index, segment in enumerate(self.output_segments):
            yield index + 1, segment, self.track_names[index]


def split_gpx(
    source_path: Path, target_directory: Path, max_segment_points: int = 500
) -> None:
    gpx = parse_gpx(source_path.read_text())

    splitter = SplitGpx()
    splitter.generate_segments(gpx=gpx, max_segment_points=max_segment_points)
    output_template = get_filename_template(source_path, splitter.segment_count)
    name_templates = splitter.get_name_templates()
    name_counts = {name: 1 for name in set(splitter.track_names)}
    for index, segment, old_name in splitter.get_enumerated_segments():
        new_name = name_templates[old_name].format(index=name_counts[old_name])
        name_counts[old_name] += 1
        output_gpx = GPX()
        output_gpx.name = new_name
        gpx_track = GPXTrack(name=new_name)
        output_gpx.tracks.append(gpx_track)
        gpx_track.segments.append(segment)

        filename = output_template.format(index=index)
        (target_directory / filename).write_text(output_gpx.to_xml())
