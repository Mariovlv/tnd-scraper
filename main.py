import requests
from bs4 import BeautifulSoup
import spotipy
import wikipedia
from dotenv import load_dotenv
import os

# Load API keys from .env file
load_dotenv()

# Scraping The Needle Drop website for reviews
def scrape_needle_drop_reviews():
    url = 'https://www.theneedledrop.com/'
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    title_links = soup.find_all('a', class_='summary-title-link')

    albums = [link.get_text() for link in title_links[:5]]
    return albums

# Authenticating with the Spotify API
def authenticate_spotify():
    # Retrieve Spotify API credentials from environment variables
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    # Authenticate with the Spotify API
    sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    return sp

# Searching for album information
def search_album_info(sp, album_name):
    # Search for the album on Spotify
    results = sp.search(q=album_name, type='album', limit=1)

    if 'albums' not in results or 'items' not in results['albums'] or len(results['albums']['items']) == 0:
        print(f"No album found for '{album_name}' on Spotify.\n")
        return

    # Get the Spotify album ID
    album_id = results['albums']['items'][0]['id']

    # Get the album's Wikipedia page title
    album_title = results['albums']['items'][0]['name']
    wiki_page_title = f'{album_title} (album)'

    # Search for the album's Wikipedia page and get its summary text
    try:
        wiki_page = wikipedia.page(wiki_page_title)
        summary_text = wikipedia.summary(wiki_page_title)
    except wikipedia.exceptions.PageError:
        summary_text = 'No Wikipedia page found for this album.'

    # Print the album name and summary text
    print(f'{album_name}:\n{summary_text}\n')

# Main function
def main():
    albums = scrape_needle_drop_reviews()

    # Authenticate with Spotify
    sp = authenticate_spotify()

    # Call the search_album_info function for each album/EP
    for album in albums:
        search_album_info(sp, album)

if __name__ == "__main__":
    main()
