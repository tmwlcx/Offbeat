import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pymysql
import config

input_file = ''

conn = pymysql.connect('35.196.88.209', 'teameleven', 'dbpassword', 'SPOTIFY')
cur = conn.cursor()
sql = "select artist_uri from artist where artist_id not in (select artist_id from album) ORDER BY artist_uri;"

cur.execute(sql)

artist_uris = cur.fetchall()

artist_uris = [row[0] for row in artist_uris]

client_credentials_manager = SpotifyClientCredentials(client_id=config.client_id,
                                                      client_secret=config.client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

for artist_uri in artist_uris:
    albums = sp.artist_albums(artist_uri)

    # If nothing is returned from search, skip
    if len(albums['items']) == 0:
        print('break')
        continue

    albums = [(album['id'], album['name']) for album in albums['items']][:10]
    print(artist_uri)
    for album in albums:
        artist_id = artist_uri.split(':')[-1]
        album_id = album[0]
        album_name = album[1]

        album = (album_id, artist_id, album_name, 'spotify:album:'+album_id)

        sql = """ INSERT INTO album(album_id,artist_id,album_name,album_uri) 
                  VALUES (%s,%s,%s,%s) """ 
        cur = conn.cursor()
        cur.execute(sql, album)
        conn.commit()

        album_tracks = sp.album_tracks(album_id)

        # If nothing is returned from search, skip
        if len(album_tracks['items']) == 0:
            print('break')
            continue

        for track in album_tracks['items']:

            song_uri = track['uri']
            song_id = track['id']
            song_name = track['name']
            audio_feature = sp.audio_features(song_id)[0]
            # If nothing is returned from search, skip
            if not audio_feature:
                print('break')
                continue

            duration_ms = audio_feature['duration_ms']
            track_href = audio_feature['track_href']
            danceability = audio_feature['danceability']
            musical_key = audio_feature['key']
            energy = audio_feature['energy']
            loudness = audio_feature['loudness']
            mode = audio_feature['mode']
            speechiness = audio_feature['speechiness']
            acousticness = audio_feature['acousticness']
            instrumentalness = audio_feature['instrumentalness']
            liveness = audio_feature['liveness']
            valence = audio_feature['valence']
            tempo = audio_feature['tempo']
            time_signature = audio_feature['time_signature']
            song =  (
                        song_id, song_name, artist_id, album_id,
                        track_href, duration_ms, danceability, energy, 
			musical_key, loudness, mode, speechiness,
                        acousticness, instrumentalness, liveness,
                        valence, tempo, time_signature
                    )

            sql = """ INSERT INTO songs(song_id, song_name, artist_id, album_id, 
                                        track_href, duration_ms, danceability, energy, 
                                        musical_key, loudness, mode, speechiness, acousticness, 
                                        instrumentalness, liveness, valence, tempo, time_signature)
                      VALUES (%s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s)"""
            cur = conn.cursor()
            cur.execute(sql, song)
            conn.commit()
