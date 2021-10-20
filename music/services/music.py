import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def find_musics(query):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="8939ec4ebe5b4399af210a2d1f781267",
                                                           client_secret="34b6defc271e4362805da7e286c380a1"))
    playlist = []
    results = sp.search(q=query, limit=20)

    for track in results['tracks']['items']:
        playlist.append(track['name'])

    return playlist