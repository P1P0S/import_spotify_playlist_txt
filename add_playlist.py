import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from os import getenv

load_dotenv()

auth_manager = SpotifyOAuth(
    client_id=getenv('CLIENT_ID'),
    client_secret=getenv('CLIENT_SECRET'),
    redirect_uri='http://localhost:8888/callback',
    scope='playlist-modify-public'
)

spotify = spotipy.Spotify(auth_manager=auth_manager)

with open('songs.txt', 'r') as f:
    songs = f.read().splitlines()

song_ids = []

for song in songs:
    result = spotify.search(q=song, limit=1)
    if result['tracks']['total'] > 0:
        for idx, track in enumerate(result['tracks']['items']):
            print(idx, track['name'])
            song_ids.append(track['id'])
    else:
        print(f"A música '{song}' não foi encontrada.")

spotify.playlist_add_items(
    playlist_id=getenv(
        'YOUR_PLAYLIST_ID'),
    items=song_ids
)
