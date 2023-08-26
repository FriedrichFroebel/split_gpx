from pathlib import Path

from faker import Faker
from gpxpy.gpx import GPX, GPXTrack, GPXTrackSegment, GPXTrackPoint


TARGET_DIRECTORY = Path(__file__).parent.parent / "tests" / "examples"


def main():
    fake = Faker()

    gpx = GPX()

    # First track: Unnamed.
    gpx_track = GPXTrack()
    gpx.tracks.append(gpx_track)
    gpx_segment = GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    for _ in range(1337):
        latitude, longitude = fake.latlng()
        gpx_segment.points.append(
            GPXTrackPoint(latitude=float(latitude), longitude=float(longitude))
        )

    # Second track: Named.
    gpx_track = GPXTrack(name="My test name")
    gpx.tracks.append(gpx_track)
    gpx_segment = GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    for _ in range(1000):
        latitude, longitude = fake.latlng()
        gpx_segment.points.append(
            GPXTrackPoint(latitude=float(latitude), longitude=float(longitude))
        )

    target_file = TARGET_DIRECTORY / "basic" / "my_track.gpx"
    target_file.write_text(gpx.to_xml())


if __name__ == "__main__":
    main()
