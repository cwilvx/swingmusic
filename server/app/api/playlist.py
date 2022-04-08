"""
Contains all the playlist routes.
"""
from app import api
from app import exceptions
from app import instances
from app import models
from app import serializer
from app.lib import playlistlib
from flask import Blueprint
from flask import request

playlist_bp = Blueprint("playlist", __name__, url_prefix="/")

PlaylistExists = exceptions.PlaylistExists
TrackExistsInPlaylist = exceptions.TrackExistsInPlaylist


@playlist_bp.route("/playlists", methods=["GET"])
def get_all_playlists():
    return {"data": [serializer.Playlist(p) for p in api.PLAYLISTS]}


@playlist_bp.route("/playlist/new", methods=["POST"])
def create_playlist():
    data = request.get_json()

    playlist = {
        "name": data["name"],
        "description": "",
        "pre_tracks": [],
        "lastUpdated": 0,
        "image": "",
    }

    try:
        for pl in api.PLAYLISTS:
            if pl.name == playlist["name"]:
                raise PlaylistExists("Playlist already exists.")

    except PlaylistExists as e:
        return {"error": str(e)}, 409

    upsert_id = instances.playlist_instance.insert_playlist(playlist)
    p = instances.playlist_instance.get_playlist_by_id(upsert_id)
    pp = models.Playlist(p)

    api.PLAYLISTS.append(pp)

    return {"playlist": pp}, 201


@playlist_bp.route("/playlist/<playlist_id>/add", methods=["POST"])
def add_track_to_playlist(playlist_id: str):
    data = request.get_json()

    trackid = data["track"]

    try:
        playlistlib.add_track(playlist_id, trackid)
    except TrackExistsInPlaylist as e:
        return {"error": str(e)}, 409

    return {"msg": "I think It's done"}, 200


@playlist_bp.route("/playlist/<playlistid>")
def get_single_p_info(playlistid: str):
    for p in api.PLAYLISTS:
        if p.playlistid == playlistid:
            tracks = p.get_tracks()
            return {"info": serializer.Playlist(p), "tracks": tracks}

    return {"info": {}, "tracks": []}


@playlist_bp.route("/playlist/<playlistid>/update", methods=["PUT"])
def update_playlist(playlistid: str):
    image = None

    if "image" in request.files:
        image = request.files["image"]

    data = request.form

    print(type(image))
    print(image.content_type)

    playlist = {
        "name": str(data.get("name")).strip(),
        "description": str(data.get("description").strip()),
        "lastUpdated": str(data.get("lastUpdated")),
        "image": None,
    }

    if image:
        playlist["image"] = playlistlib.save_p_image(image, playlistid)

    for p in api.PLAYLISTS:
        if p.playlistid == playlistid:
            p.update_playlist(playlist)
            instances.playlist_instance.update_playlist(playlistid, playlist)

            return {
                "data": serializer.Playlist(p),
            }

    return {"msg": "Something shady happened"}, 500


# @playlist_bp.route("/playlist/<playlist_id>/info")
# def get_playlist_track(playlist_id: str):
#     tracks = playlistlib.get_playlist_tracks(playlist_id)
#     return {"data": tracks}
