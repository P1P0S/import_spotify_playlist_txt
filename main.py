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

# TODO: Fix magic number
min_precision = 0.4

for song in songs:
    tracks = search_tracks(spotify, song, limit=5)

    if tracks:
        best_match = None
        best_match_score = 0

        for track in tracks:
            similarity_score, track_name = similar(
                song.lower(), track['name'].lower())
            if similarity_score > best_match_score and \
                    similarity_score >= min_precision:
                best_match = track
                best_match_score = similarity_score

        if best_match:
            print(f"\033[32mSong:\033[0m {best_match['name']} "
                  f"\033[32m[precision - "
                  f"{best_match_score * 100:.0f}%]\033[0m")
            song_ids.append(best_match['id'])
        else:
            print(f"\033[31mSong:\033[0m {song} \033[31m[not found]")

if song_ids:
    playlist_id = getenv('YOUR_PLAYLIST_ID')
    playlist_add_tracks(spotify, playlist_id, song_ids)
