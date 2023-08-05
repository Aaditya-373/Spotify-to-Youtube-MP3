import requests
import base64
import json

client_id = 'dbc38c0d43e74821ae7f87ae82efb8c8'
client_secret = '253d96d51cab4a618d324d6d35d8cf6f'
token_url = "https://accounts.spotify.com/api/token"
method = "POST"


def get_token():
    token_data = {
        "grant_type": "client_credentials"
    }
    client_credentials = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_credentials.encode())

    token_headers = {
        "Authorization":f"Basic {client_creds_b64.decode()}"
    }
    r = requests.post(token_url,data  = token_data,headers = token_headers)
    token_response_data = r.json()
    token = token_response_data['access_token']
    return token



def get_auth_header(token):
    return {"Authorization":"Bearer "+token}

def get_user_id(user_email,token):
    url = f'https://api.spotify.com/v1/me'
    header = get_auth_header(token)
    response = requests.get(url,headers = header)
    if response.status_code == 200:
        user_data = response.json()
        print(user_data)
    return None
    
        
    
    
# def get_user_playlists(token,user_id):
#     url = f'https://api.spotify.com/v1/{user_id}/playlists'
#     get_response = requests.get(url,headers = get_auth_header(token))
#     playlists_data = get_response.json()
#     return playlists_data

# get_user_playlists(token,user_id)
#We need to get user_id from these two information
token = get_token()
user_name = input("Enter Spotify username: ")
email = input("Enter your email id: ")
print(get_user_id(user_name,email,token))





















