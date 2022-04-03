"""
This library contains all the functions related to albums.
"""

import urllib
from pprint import pprint
from typing import List

from app import api, functions, models
from app.lib import trackslib


def create_everything() -> List[models.Track]:
    """
    Creates album objects for all albums and returns
    a list of track objects
    """
    albums: list[models.Album] = functions.get_all_albums()

    api.ALBUMS.clear()
    api.ALBUMS.extend(albums)

    tracks = trackslib.create_all_tracks()

    api.TRACKS.clear()
    api.TRACKS.extend(tracks)


def get_album_duration(album: list) -> int:
    """
    Gets the duration of an album.
    """

    album_duration = 0

    for track in album:
        album_duration += track["length"]

    return album_duration


def get_album_image(album: list) -> str:
    """
    Gets the image of an album.
    """

    for track in album:
        img_p = (track["album"] + track["albumartist"] + ".webp").replace("/", "::")
        img = functions.extract_thumb(track["filepath"], webp_path=img_p)

        if img is not None:
            return img

    return functions.use_defaults()


def get_album_tracks(album: str, artist: str) -> List:
    tracks = []

    for track in api.PRE_TRACKS:
        try:
            if track["album"] == album and track["albumartist"] == artist:
                tracks.append(track)
        except TypeError:
            pprint(track, indent=4)
            print(album, artist)
    return tracks


def create_album(track) -> models.Album:
    """
    Generates and returns an album object from a track object.
    """
    album = {
        "album": track["album"],
        "artist": track["albumartist"],
    }

    album_tracks = get_album_tracks(album["album"], album["artist"])

    album["count"] = len(album_tracks)
    album["duration"] = get_album_duration(album_tracks)
    album["date"] = album_tracks[0]["date"]

    album["artistimage"] = urllib.parse.quote_plus(
        album_tracks[0]["albumartist"] + ".webp"
    )

    album["image"] = get_album_image(album_tracks)

    return models.Album(album)


def find_album(albumtitle, artist):
    for album in api.ALBUMS:
        if album.album == albumtitle and album.artist == artist:
            return album


def search_albums_by_name(query: str) -> List[models.Album]:
    """
    Searches albums by album name.
    """
    title_albums: List[models.Album] = []
    artist_albums: List[models.Album] = []

    for album in api.ALBUMS:
        if query.lower() in album.album.lower():
            title_albums.append(album)

    for album in api.ALBUMS:
        if query.lower() in album.artist.lower():
            artist_albums.append(album)

    return [*title_albums, *artist_albums]
