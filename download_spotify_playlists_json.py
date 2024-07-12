import asyncio
import json
import os

import spotipy
import yaml
from spotify_to_tidal import auth, sync


def save_all_spotify_playlist_to_json_files(spotify_session: spotipy.Spotify, config):
    os.makedirs("playlists", exist_ok=True)
    playlists = asyncio.run(sync.get_playlists_from_spotify(spotify_session, config))
    # add the tracks to the playlist
    for playlist in playlists:
        playlist["tracks"] = asyncio.run(
            sync.get_tracks_from_spotify_playlist(spotify_session, playlist)
        )
        # handle slashes in the playlist name
        file_path = f"{playlist['name']}.json"
        file_path = file_path.replace("/", "-")
        file_path = os.path.join("playlists", file_path)
        with open(file_path, "w") as f:
            print(f'Saving playlist "{playlist["name"]} with id {playlist["id"]}')
            f.write(json.dumps(playlist, indent=4))


if __name__ == "__main__":
    config_path = "config.yml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    print("Opening Spotify session")

    spotify_session = auth.open_spotify_session(config["spotify"])
    save_all_spotify_playlist_to_json_files(spotify_session, config)
