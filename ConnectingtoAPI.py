import spotify_config as spc
import pandas as pd

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Authentication - without user
client_credentials = SpotifyClientCredentials(client_id=spc.spotify_client_id,
                                              client_secret=spc.spotify_client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials)

# Playlist link you want to work with - TOP SONGS GLOBAL
playlist_link = 'https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF'
playlist_URI = '37i9dQZEVXbNG2KDcFcKOF'

top_songs = sp.playlist_items(playlist_id='37i9dQZEVXbNG2KDcFcKOF')
# this is a dict, we are interested in 'items'

top_songs_items = sp.playlist_items(playlist_id='37i9dQZEVXbNG2KDcFcKOF')['items']

# obtaining track/album/artist info

# trying different way: define empty dict with relevant keys

track = {'track_URI': [], 'track_name': [], 'track_popularity': [],
         'album_URI': [], 'album_name': [], 'album_date': [], 'album_ntracks': [],
         'artist_1_URI': [], 'artist_1_name': [], 'artist_2_URI': [], 'artist_2_name': []
         }

for song in top_songs_items:

    # track info
    track['track_URI'].append(song['track']['uri'])
    track['track_name'].append(song['track']['name'])
    track['track_popularity'].append(song['track']['popularity'])

    # album info
    track['album_URI'].append(song['track']['album']['uri'])
    track['album_name'].append(song['track']['album']['name'])
    track['album_date'].append(song['track']['album']['release_date'])
    track['album_ntracks'].append(song['track']['album']['total_tracks'])

    # artist info (only considering 1st & 2nd artists)
    track['artist_1_URI'].append(song['track']['artists'][0]['uri'])
    track['artist_1_name'].append(song['track']['artists'][0]['name'])

    try:
        track['artist_2_URI'].append(song['track']['artists'][1]['uri'])
        track['artist_2_name'].append(song['track']['artists'][1]['name'])

    except IndexError:
        track['artist_2_URI'].append('null')
        track['artist_2_name'].append('null')

# converting list of dict -> df
track_df = pd.DataFrame.from_dict(track)

# obtaining audio features based on track URI

# returns list of dict -> then -> converting dict to dataframe
audio_features = pd.DataFrame.from_dict(sp.audio_features(track['track_URI']))

print(track_df.head())

# todo revise this code for more songs