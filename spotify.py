import requests
import base64
from datetime import timedelta, datetime    
    
class Spotify:
    def __init__(self):
        self.CLIENT_ID          = ""
        self.CLIENT_SECRET      = ""
        
        self.API_ENDPOINT       = "https://api.spotify.com/v1/"
        self.AUTH_ENDPOINT      = "https://accounts.spotify.com/authorize"
        self.GET_TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"
        self.REDIRECT_URI       = "http://127.0.0.1:5000/"
        
        ####################################################################
        
        self.spotify_data = {}
        
        ####################################################################
        
    def get_oauth2_url(self) -> str:
        scopes = ["user-read-playback-state", "user-modify-playback-state", "user-read-currently-playing", "user-read-private", "user-read-email"]
        
        url = requests.Request("GET", self.AUTH_ENDPOINT, params={
            "client_id": self.CLIENT_ID,
            "response_type": "code",
            "redirect_uri": self.REDIRECT_URI,
            "scope": " ".join(scopes)
        }).prepare().url
        
        self.spotify_data["is_authenticated"] = True
        
        return url
    
    def get_or_refresh_access_token(self, _type = None, auth_code = None) -> None:
        auth_string = self.CLIENT_ID + ":" + self.CLIENT_SECRET
        auth_base64 = str(base64.b64encode(auth_string.encode("utf-8")), "utf-8")
        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content": "application/x-www-form-urlencoded"
        }
        
        if _type == "GET" and auth_code is not None:
            data = {
                "code": auth_code,
                "grant_type": "authorization_code",
                "redirect_uri": self.REDIRECT_URI 
            }
        else:
            data = {
                "grant_type": "refresh_token",
                "refresh_token": self.spotify_data['refresh_token']
            }
    
        response = requests.post(self.GET_TOKEN_ENDPOINT, headers=headers, data=data).json()
        
        self.spotify_data["expires_in"]     = datetime.now() + timedelta(seconds=response.get("expires_in"))
        self.spotify_data["access_token"]   = response.get("access_token")
        try:
            self.spotify_data["refresh_token"]  = response.get("refresh_token")
        except:
            pass
        self.spotify_data['is_authenticated'] = True
    
    def is_authenticated(self) -> bool:
        if not "is_authenticated" in self.spotify_data:
            return False
        return True
    
    def is_token_expired(self) -> bool:
        if not "expires_in" in self.spotify_data or self.spotify_data['expires_in'] <= datetime.now():
            return True
        return False
    
    def get_playlist(self, playlist_id) -> list:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.spotify_data['access_token']}"
        }
        query_param = self.API_ENDPOINT + f"playlists/{playlist_id}/tracks"
        response = requests.get(query_param, headers=headers)
        print(response.json())
        music_ids = []
        for music in response.json()['items']:
                music_ids.append(music['track']['id'])
        return music_ids