import re

def extract_artist_id(url):
    match = re.search(r'artist/([a-zA-Z0-9]+)', url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid Spotify artist URL")

# Example usage
url = 'https://open.spotify.com/artist/0QHgL1lAIqAw0HtD7YldmP?autoplay=true'
artist_id = extract_artist_id(url)
print(artist_id)  # Output: 0QHgL1lAIqAw0HtD7YldmP
