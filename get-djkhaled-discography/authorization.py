import requests
import webbrowser
from urllib.parse import urlencode, parse_qs, urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer

# Define your Spotify API credentials and redirect URI
client_id = 'eb887208709d4b14a2b86e097fd54cdb'
client_secret = 'GET-YOUR-OWN-CLIENT-SECRET-DIPSHIT'
redirect_uri = 'http://localhost:8080/callback'
scopes = 'user-library-read'

# Step 1: Authorize
auth_url = 'https://accounts.spotify.com/authorize'
params = {
    'response_type': 'code',
    'client_id': client_id,
    'scope': scopes,
    'redirect_uri': redirect_uri
}

auth_request_url = f"{auth_url}?{urlencode(params)}"
print(f"Opening the following URL in the browser for authorization: {auth_request_url}")
webbrowser.open(auth_request_url)

# Step 2: Handle Redirect
class SpotifyAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        code = query_components.get('code')
        if code:
            code = code[0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Authorization successful! You can close this window.')
            print(f"Authorization code received: {code}")
            # Exchange the authorization code for an access token
            exchange_token(code)
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Authorization failed! No code received.')
            print("Authorization failed! No code received.")

def run(server_class=HTTPServer, handler_class=SpotifyAuthHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Waiting for authorization...')
    httpd.handle_request()

def exchange_token(auth_code):
    token_url = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(token_url, data=payload, headers=headers)
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data['access_token']
        print(f"Access Token: {access_token}")
    else:
        print(f"Failed to get access token. Status code: {response.status_code}, Response: {response.text}")

if __name__ == '__main__':
    run()
