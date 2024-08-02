import requests

access_token = 'GET-YOUR-OWN-TOKEN-DIPSHIT'
artist_id = '0QHgL1lAIqAw0HtD7YldmP'

# Define the base URL for Spotify Web API
base_url = 'https://api.spotify.com/v1'

# Function to get the artist's albums
def get_artist_albums(artist_id):
    albums = []
    url = f'{base_url}/artists/{artist_id}/albums'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    while url:
        response = requests.get(url, headers=headers)
        response_data = response.json()
        albums.extend(response_data['items'])
        url = response_data.get('next')  # Get the next page of results

    return albums

# Function to get tracks from an album
def get_album_tracks(album_id):
    tracks = []
    url = f'{base_url}/albums/{album_id}/tracks'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    while url:
        response = requests.get(url, headers=headers)
        response_data = response.json()
        tracks.extend(response_data['items'])
        url = response_data.get('next')  # Get the next page of results

    return tracks

# Get all albums for the artist
albums = get_artist_albums(artist_id)

# Collect all tracks and their links
tracks_info = []

for album in albums:
    album_id = album['id']
    album_name = album['name']
    album_url = album['external_urls']['spotify']
    print(f'Album: {album_name} ({album_url})')
    
    tracks = get_album_tracks(album_id)
    for track in tracks:
        track_name = track['name']
        track_url = track['external_urls']['spotify']
        tracks_info.append((track_name, track_url, album_name, album_url))

# Write the track information to a text file with UTF-8 encoding
with open('artist_tracks.txt', 'w', encoding='utf-8') as f:
    for track_name, track_url, album_name, album_url in tracks_info:
        f.write(f'Track: {track_name}\n')
        f.write(f'URL: {track_url}\n')
        f.write(f'Album: {album_name}\n')
        f.write(f'Album URL: {album_url}\n')
        f.write('\n')
        
print('Track information has been written to artist_tracks.txt')
