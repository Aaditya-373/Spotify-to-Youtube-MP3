from flask import Flask,url_for,redirect,request,session
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials,SpotifyOAuth
import requests
import time
import csv

app = Flask(__name__)
app.secret_key = 'rameshasfiofafapooluwognqwkefsunniaefgnjegaa'
app.config['SESSION_COOKIE_NAME'] = 'spotifyprojcookei'
@app.route('/')
def home():
    return "Welcome <a href = '/login'>Click to Login with Spotify</a>"

@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    authorization_url = sp_oauth.get_authorize_url()
    return redirect(authorization_url)
    

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    access_token = token_info['access_token']
    session['token_info'] = token_info
    return redirect(url_for('getuserTracks',_external = True))


@app.route('/getuserTracks')
def getuserTracks():
    try:
        token_info = get_token()
    except:
        print("USER NOT LOGGED IN")
        redirect('/login')
    sp = spotipy.Spotify(auth= token_info['access_token'])
    
    playlists = sp.current_user_playlists(limit=20,offset = 0)
    user_data = {}
    for playlist in playlists['items']:
        playlist_name = playlist['name']
        playlist_id = playlist['id']
        playlist_songs = []
        tracks = sp.playlist_tracks(playlist_id)
        for item in tracks['items']:
            track = item['track']
            playlist_songs.append(track['name'])
        user_data[playlist_name] = playlist_songs
    with open('playlist_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        playlist = input("Enter the playlist you want to download:")
        for pn, s in user_data.items():
           writer.writerow([pn])
    
            
    return user_data

def get_token():
    token_info = session.get('token_info',None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now<60
    if(is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info
client_id = 'dbc38c0d43e74821ae7f87ae82efb8c8'
client_secret = '253d96d51cab4a618d324d6d35d8cf6f'


def create_spotify_oauth():
    return SpotifyOAuth(client_id="dbc38c0d43e74821ae7f87ae82efb8c8",client_secret="253d96d51cab4a618d324d6d35d8cf6f",redirect_uri=url_for('redirectPage',_external = True),scope="user-library-read user-read-email playlist-read-private playlist-read-collaborative playlist-modify-public")




if __name__ == '__main__':
    app.run(debug=True)


