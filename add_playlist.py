import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from os import getenv
import difflib

load_dotenv()

auth_manager = SpotifyOAuth(
    client_id=getenv('CLIENT_ID'),
    client_secret=getenv('CLIENT_SECRET'),
    redirect_uri='http://localhost:8888/callback',
    scope='playlist-modify-public'
)

spotify = spotipy.Spotify(auth_manager=auth_manager)


def similar(a, b):
    similarity_score = difflib.SequenceMatcher(None, a, b).ratio()
    return similarity_score, b


with open('songs.txt', 'r') as f:
    songs = f.read().splitlines()

song_ids = []

for song in songs:
    result = spotify.search(q=song, limit=5)
    if result['tracks']['total'] > 0:
        best_match = None
        best_match_score = 0
        for idx, track in enumerate(result['tracks']['items']):
            similarity_score, track_name = similar(
                song.lower(), track['name'].lower())
            if similarity_score > best_match_score:
                best_match = track
                best_match_score = similarity_score

        if best_match:
            print(f"{best_match['name']} - {best_match_score * 100:.2f}%")
            song_ids.append(best_match['id'])
        else:
            print(f"The music '{song}' was not found.")
    else:
        print(f"The music '{song}' was not found.")

spotify.playlist_add_items(
    playlist_id=getenv('YOUR_PLAYLIST_ID'),
    items=song_ids)
