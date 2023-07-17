import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from os import getenv

load_dotenv()


def create_spotify_instance():
    auth_manager = SpotifyOAuth(
        client_id=getenv('CLIENT_ID'),
        client_secret=getenv('CLIENT_SECRET'),
        redirect_uri='http://localhost:8888/callback',
        scope='playlist-modify-public'
    )
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify


def search_tracks(spotify, query, limit=5):
    result = spotify.search(q=query, limit=limit)
    return result['tracks']['items'] if 'tracks' in result else []


def playlist_add_tracks(spotify, playlist_id, track_ids):
    spotify.playlist_add_items(playlist_id=playlist_id, items=track_ids)
