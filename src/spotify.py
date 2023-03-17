import os
import pandas as pd
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

if __name__ == "__main__":
    spotify_playlist = SpotifyPlaylist()
    spotify_playlist.main()
