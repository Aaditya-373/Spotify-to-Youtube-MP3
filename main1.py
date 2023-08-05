from flask import Flask,request,url_for,redirect
import spotipy
import requests 
import base64
import json

app = Flask(__name__)

#App credentials
client_id = 'dbc38c0d43e74821ae7f87ae82efb8c8'
client_secret = '253d96d51cab4a618d324d6d35d8cf6f'
redirect_uri = 'http://127.0.0.1:5000'

token_url = "https://accounts.spotify.com/api/token"
authorize_url = "https://accounts.spotify.com/authorize"

scope = 'user-library-read user-read-email playlist-read-private playlist-read collaborative playlist-modify-public'
def get_token(code):
    token_data = {
        "grant_type":"authorization_code",
        "code":code,
        "redirect_uri":redirect_uri
    }
    client_credentials  = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_credentials.encode())
    token_headers = {
        "Authorization":f"Base {client_creds_b64.decode()}"
    }

    response = requests.post(token_url,data = token_data,headers = token_headers)
    response_data = response.json()
    return response_data['access_token']


#Authorization route
@app.route('/authorize')
def authorize():
    params = {
        'client_id':client_id,
        'response_type': 'code',
        'redirect_uri':redirect_uri,
        'scope': scope
    }
    authorize_url_with_params = f"{authorize_url}?{requests.compat.urlencode(params)}"

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token = get_token(code)

    if token is not None:
        # Use the token to make API requests
        # You can store the token in a session or a database for further use
        return "Authorization successful! Access token: " + token
    else:
        return "Authorization failed!"

if __name__ == '__main__':
    app.run(debug = True)
