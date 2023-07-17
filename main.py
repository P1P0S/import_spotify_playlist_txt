import difflib
from os import getenv
from spotify_utils import create_spotify_instance, \
    search_tracks, \
    playlist_add_tracks


def similar(a, b):
    similarity_score = difflib.SequenceMatcher(None, a, b).ratio()
    return similarity_score, b


with open('songs.txt', 'r') as f:
    songs = f.read().splitlines()

spotify = create_spotify_instance()

song_ids = []

for song in songs:
    tracks = search_tracks(spotify, song, limit=5)

    if tracks:
        best_match = None
        best_match_score = 0

        for track in tracks:
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

if song_ids:
    playlist_id = getenv('YOUR_PLAYLIST_ID')
    playlist_add_tracks(spotify, playlist_id, song_ids)
