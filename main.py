import os
import json
import pandas as pd
from ytmusicapi import YTMusic
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyPlaylist:
    def __init__(self):
        self.auth_manager = SpotifyOAuth(
            client_id="a9dbb7c458dd48db945111d11423b89e",
            client_secret="ed96e0515a1b4a5385462dff86f5e4bb",
            redirect_uri="http://localhost:8000/callback/",
            scope=[
                "user-library-read",
                "playlist-read-private",
                "playlist-modify-private",
                "playlist-modify-public",
            ],
        )
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)

    def get_playlist_tracks(self, playlist_id):
        tracks = self.sp.playlist_tracks(playlist_id, limit=50)
        all_tracks = tracks["items"]
        while tracks["next"]:
            tracks = self.sp.next(tracks)
            all_tracks.extend(tracks["items"])
        return all_tracks

    def main(self):
        playlists = self.sp.current_user_playlists()["items"]

        if not os.path.exists("playlist"):
            os.mkdir("playlist")

        for playlist in playlists:
            playlist_name = playlist["name"]
            playlist_id = playlist["id"]
            all_tracks = self.get_playlist_tracks(playlist_id)

            playlist_songs = [
                {
                    "song_name": t["track"]["name"],
                    "artist_name": t["track"]["artists"][0]["name"],
                }
                for t in all_tracks
            ]

            df = pd.DataFrame(playlist_songs)
            df.to_csv(
                f"playlist/{playlist_name}.csv",
                index=False,
                encoding="utf-8",
                header=None,
            )

class PlaylistImporter:
    def __init__(self, headers_auth_path):
        self.ytmusic = YTMusic(headers_auth_path)
        if not os.path.exists('log'):
            os.makedirs('log')
        self.stored_playlist_id = self._load_playlist_ids()

    def _load_playlist_ids(self):
        try:
            with open('log/playlist_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_playlist_ids(self):
        with open('log/playlist_data.json', 'w') as f:
            json.dump(self.stored_playlist_id, f)

    def _get_or_create_playlist(self, playlist_name):
        if playlist_name in self.stored_playlist_id:
            print(f"Playlist {playlist_name} already exists")
            return self.stored_playlist_id[playlist_name]
        else:
            playlist_id = self.ytmusic.create_playlist(playlist_name, 'created by https://github.com/Mai0313')
            self.stored_playlist_id[playlist_name] = playlist_id
            self._save_playlist_ids()
            print(f"Playlist {playlist_name} has been created and saved to playlist_data.json")
            return playlist_id

    def import_playlist(self, filename):
        data = pd.read_csv(f'playlist/{filename}', header=None).values.tolist()
        playlist_name = filename[:-4]
        playlist_id = self._get_or_create_playlist(playlist_name)

        for music, artist in data:
            search_results = self.ytmusic.search(f'{music} {artist}', filter='songs')
            video_id = search_results[0]['videoId']
            self.ytmusic.add_playlist_items(playlist_id, [video_id])
            print(f"{music} by {artist} has been added successfully to {filename}")

    def import_all_playlists(self):
        filenames = [f for f in os.listdir('playlist') if f.endswith('.csv')]

        for filename in filenames:
            self.import_playlist(filename)
            print(f"{filename} has been added to YouTube Music successfully")
            
            

if __name__ == "__main__":
    spotify_playlist = SpotifyPlaylist()
    spotify_playlist.main()
    
    importer = PlaylistImporter('script/headers_auth.json')
    importer.import_all_playlists()
