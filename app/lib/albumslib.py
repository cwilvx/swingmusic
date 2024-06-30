"""
Contains methods relating to albums.
"""

from dataclasses import asdict
from typing import Any
from itertools import groupby


from app.models.track import Track
from app.store.albums import AlbumStore
from app.store.tracks import TrackStore


def remove_duplicate_on_merge_versions(tracks: list[Track]) -> list[Track]:
    """
    Removes duplicate tracks when merging versions of the same album.
    """
    # TODO!
    pass


def sort_by_track_no(tracks: list[Track]):
    # tracks = [asdict(t) for t in tracks]

    for t in tracks:
        track = str(t.track).zfill(3)
        t._pos = int(f"{t.disc}{track}")

    tracks = sorted(tracks, key=lambda t: t._pos)

    return tracks
