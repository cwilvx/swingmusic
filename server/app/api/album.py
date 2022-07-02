"""
Contains all the album routes.
"""
from pprint import pprint
from typing import List

from app import api
from app import helpers
from app import models
from app.lib import albumslib
from flask import Blueprint
from flask import request
from app.functions import FetchAlbumBio
from app import instances

album_bp = Blueprint("album", __name__, url_prefix="")


@album_bp.route("/")
def say_hi():
    """Returns some text for the default route"""
    return "^ _ ^"


@album_bp.route("/albums")
def get_albums():
    """returns all the albums"""
    albums = []

    for song in api.DB_TRACKS:
        al_obj = {"name": song["album"], "artist": song["artists"]}

        if al_obj not in albums:
            albums.append(al_obj)

    return {"albums": albums}


@album_bp.route("/album", methods=["POST"])
def get_album():
    """Returns all the tracks in the given album."""
    data = request.get_json()
    albumhash = data["hash"]
    error_msg = {"error": "Album not created yet."}

    tracks = instances.tracks_instance.find_tracks_by_hash(albumhash)

    if len(tracks) == 0:
        return error_msg, 204

    tracks = [models.Track(t) for t in tracks]
    tracks = helpers.RemoveDuplicates(tracks)()

    album = instances.album_instance.find_album_by_hash(albumhash)

    if not album:
        return error_msg, 204

    album = models.Album(album)

    album.count = len(tracks)
    try:
        album.duration = albumslib.get_album_duration(tracks)
    except AttributeError:
        album.duration = 0

    if (
        album.count == 1
        and tracks[0].title == album.title
        and tracks[0].tracknumber == 1
        and tracks[0].disknumber == 1
    ):
        album.is_single = True

    return {"tracks": tracks, "info": album}


@album_bp.route("/album/bio", methods=["POST"])
def get_album_bio():
    """Returns the album bio for the given album."""
    data = request.get_json()
    album_hash = data["hash"]
    err_msg = {"bio": "No bio found"}

    album = instances.album_instance.find_album_by_hash(album_hash)

    if album is None:
        return err_msg, 404

    bio = FetchAlbumBio(album["title"], album["artist"])()

    if bio is None:
        return err_msg, 404

    return {"bio": bio}


@album_bp.route("/album/artists", methods=["POST"])
def get_albumartists():
    """Returns a list of artists featured in a given album."""
    data = request.get_json()

    albumhash = data["hash"]

    tracks = instances.tracks_instance.find_tracks_by_hash(albumhash)
    tracks = [models.Track(t) for t in tracks]

    artists = []

    for track in tracks:
        for artist in track.artists:
            artist = artist.lower()
            if artist not in artists:
                artists.append(artist)

    final_artists = []
    for artist in artists:
        artist_obj = {
            "name": artist,
            "image": helpers.create_safe_name(artist) + ".webp",
        }
        final_artists.append(artist_obj)

    return {"artists": final_artists}
