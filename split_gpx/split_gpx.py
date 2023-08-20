from __future__ import annotations

from pathlib import Path

import gpxpy
import gpxpy.gpx


def get_int_length(value: int) -> int:
    return value // 10 + 1


def get_filename_template(source_path: Path, segment_count: int) -> str:
    width = get_int_length(segment_count)
    return f"{source_path.stem}_{{index:0{width}d}}{source_path.suffix}"


def get_name_template(original_name: str | None, segment_count: int) -> str:
    original_name = original_name or "(empty)"
    width = get_int_length(segment_count)
    return f"{{index:0{width}d}} - {original_name}"


def split_gpx(source_path: Path, target_directory: Path, max_segment_points: int = 500):
    gpx = gpxpy.parse(source_path.read_text())

    output_segment = gpxpy.gpx.GPXTrackSegment()
    output_segments = [output_segment]

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                output_segment.points.append(point)

                if len(output_segment.points) >= max_segment_points:
                    output_segment = gpxpy.gpx.GPXTrackSegment()
                    output_segments.append(output_segment)
                    # Make sure to the segments are connected.
                    output_segment.points.append(point)

    segment_count = len(output_segments)
    output_template = get_filename_template(source_path, segment_count)
    name_template = get_name_template(gpx.name, segment_count)
    for index, segment in enumerate(output_segments, start=1):
        new_name = name_template.format(index=index)
        output_gpx = gpxpy.gpx.GPX()
        output_gpx.name = new_name
        gpx_track = gpxpy.gpx.GPXTrack(name=new_name)
        output_gpx.tracks.append(gpx_track)
        gpx_track.segments.append(segment)

        filename = output_template.format(index=index)
        (target_directory / filename).write_text(output_gpx.to_xml())
