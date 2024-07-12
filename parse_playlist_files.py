import json
import os

from easydict import EasyDict


def parse_playlist_file(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    playlist = EasyDict()
    playlist.name = data["name"]
    playlist.id = data["id"]
    playlist.images = data["images"]
    playlist.tracks = []

    for track in data["tracks"]:
        track_data = EasyDict()
        track_data.name = track["name"]
        track_data.artists = [artist["name"] for artist in track["artists"]]
        track_data.album = track["album"]["name"]
        track_data.id = track["id"]
        playlist.tracks.append(track_data)
    return playlist


def parse_all_playlist_files():
    playlists = []
    for file in os.listdir("playlists"):
        if file.endswith(".json"):
            playlist = parse_playlist_file(os.path.join("playlists", file))
            playlists.append(playlist)
    return playlists


if __name__ == "__main__":
    playlists = parse_all_playlist_files()
    json.dump(playlists, open("playlists.json", "w"), indent=4)
