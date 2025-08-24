import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

print("🚀 It's the Time Machine 🕗🔙🕘")
# input_date = input("Which year do you want to travel to? Type the date in this formate YYY-MM-DD: ")
input_date = "2000-08-12"
BILLBOARD_URL = "https://www.billboard.com/charts/hot-100/" + input_date
HEADERS = {"USER-AGENT":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"}

response = requests.get(BILLBOARD_URL, HEADERS)

soup = BeautifulSoup(response.text, "html.parser")

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]


load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("CLIENT_ID"),
                                               client_secret=os.getenv("CLIENT_SECRET"),
                                               redirect_uri=os.getenv("REDIRECT_URL"),
                                               scope="playlist-modify-public playlist-modify-private"))

# taylor_url = 'spotify:artist:06HL4z0CvFAxyc27GXpf02'
#
# results = sp.artist_albums(taylor_url, album_type='album')
# albums = results['items']
# while results['next']:
#     results = sp.next(results)
#     albums.extend(results['items'])
#
# for album in albums:
#     print(album['name'])

# Step 1: Get user ID
user_id = sp.current_user()['id']

# Step 2: Create a new playlist
playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{input_date} 100 Billboard Playlist",
    public=False,
    description=f"Top 100 Billboard on {input_date}"
)

# Step 4: Search each song and collect track URIs
track_uris = []
for song in song_names:
    result = sp.search(q=song, type='track', limit=1)
    items = result['tracks']['items']
    if items:
        uri = items[0]['uri']
        track_uris.append(uri)
        print(f"🎵 Found: {song} -> {uri}")
    else:
        print(f"❌ Not found: {song}")



# # Step 5: Add tracks to the playlist (in batches of 100 max)
# if track_uris:
#     sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris)
#     print("✅ Tracks added to playlist!")
# else:
#     print("⚠️ No tracks found to add.")
