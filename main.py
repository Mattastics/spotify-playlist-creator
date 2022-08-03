import os
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

CLIENT_ID = "462a42a1aea246eb84141a432584f1d5"
CLIENT_SECRET = "f3225bad521f4e319837d7947dfdc429"

date = input("When do you want to travel back to? Enter in this format YYYY-MM-DD\n")
response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}")
webpage = response.text
soup = BeautifulSoup(webpage, "html.parser")
songs = soup.select(selector="li h3")

song_titles = [song.getText().strip("\n\r\t") for song in songs[:100]]
print(song_titles)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/callback",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_uris=[]
year=date.split("-")[0]
for song in song_titles:
    result= sp.search(q=f"track:{song} year:{year}", type="track")
    print (result)
    try:
        uri = result["tracls"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100")
sp.user_playlist_add_items(user=user_id, playlist_id = "0rmhjUgoVa17LZuS8xWQ3v", tracks=song_uris, position=None)