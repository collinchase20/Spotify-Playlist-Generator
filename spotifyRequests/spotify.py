from __future__ import print_function
import base64
import json
import requests
import sys

#Support both python 2 and 3
try:
    import urllib.request, urllib.error
    import urllib.parse as urllibparse
except ImportError:
    import urllib as urllibparse


#Authorization

# spotify endpoints
SPOTIFY_AUTH_BASE_URL = "https://accounts.spotify.com/{}"
SPOTIFY_AUTH_URL = SPOTIFY_AUTH_BASE_URL.format('authorize')
SPOTIFY_TOKEN_URL = SPOTIFY_AUTH_BASE_URL.format('api/token')

# client keys
CLIENT = json.load(open('conf.json', 'r+'))
CLIENT_ID = CLIENT['id']
CLIENT_SECRET = CLIENT['secret']


#REDIRECT_URI = "http://0.0.0.0:8080/callback/"
REDIRECT_URI = "http://3.18.200.191:8080/callback"
#REDIRECT_URI = "www.playlistgenerator.live:8080/callback"

#REDIRECT_URI = "http://3.18.200.191/callback"


SCOPE = "playlist-modify-public playlist-modify-private user-read-recently-played user-top-read user-library-read"

STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

# https://developer.spotify.com/web-api/authorization-guide/
auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}



#python 3
if sys.version_info[0] >= 3:
    URL_ARGS = "&".join(["{}={}".format(key, urllibparse.quote(val))
                    for key, val in list(auth_query_parameters.items())])
else: 
    URL_ARGS = "&".join(["{}={}".format(key, urllibparse.quote(val))
                    for key, val in auth_query_parameters.iteritems()])


AUTH_URL = "{}/?{}".format(SPOTIFY_AUTH_URL, URL_ARGS)



def authorize(auth_token):
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }

    base64encoded = base64.b64encode(("{}:{}".format(CLIENT_ID, CLIENT_SECRET)).encode())
    headers = {"Authorization": "Basic {}".format(base64encoded.decode())}


    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload,
                                 headers=headers)

    # tokens are returned to the app
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]

    # use the access token to access Spotify API
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    return auth_header


def get_users_profile(auth_header):
    url = "https://api.spotify.com/v1/me"
    resp = requests.get(url, headers=auth_header)
    return resp.json()


def get_users_playlists(auth_header):
    url = "https://api.spotify.com/v1/me/playlists"
    resp = requests.get(url, headers=auth_header)
    return resp.json()

def get_users_playlists_tracks(auth_header):
    url = "https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    resp = requests.get(url, headers=auth_header)
    return resp.json()

def get_users_saved_tracks(auth_header, off):
    payload = {'limit': 50, 'offset': off}
    url = "https://api.spotify.com/v1/me/tracks"
    resp = requests.get(url, headers=auth_header, params=payload)
    if not 'error' in resp.json():
        return resp.json()
    else:
        raise Exception(resp.json())

def get_songs_audio_features(auth_header, songs):
    payload = {'ids': songs}
    url = "https://api.spotify.com/v1/audio-features"
    json = requests.get(url, headers=auth_header, params=payload).json()
    return json

def make_playlist(auth_header, title, username):
    new_header = {"Authorization": auth_header["Authorization"], "Content-Type": "application/json"}
    payload = {'name': title}
    url = "https://api.spotify.com/v1/users/{}/playlists".format(username)
    resp = requests.post(url, headers=new_header, json=payload)
    if not 'error' in resp.json():
        return resp.json()
    else:
        raise Exception(resp.json())

def add_tracks_to_playlist(auth_header, id, songs):
    new_header = {"Authorization": auth_header["Authorization"], "Content-Type": "application/json"}
    payload = {'uris': songs}
    url = "https://api.spotify.com/v1/playlists/{}/tracks".format(id)
    resp = requests.post(url, headers=new_header, json=payload)
    if not 'error' in resp.json():
        return resp.json()
    else:
        raise Exception(resp.json())


def get_users_top(auth_header, t):
    if t not in ['artists', 'tracks']:
        raise Exception("Invalid Type for Top")
    url = "https://api.spotify.com/v1/me/top/{type}".format(type=t)
    resp = requests.get(url, headers=auth_header)
    return resp.json()
