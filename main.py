import requests
from bs4 import BeautifulSoup

def scrape_needle_drop_reviews():
    url = 'https://theneedledrop.com/album-reviews/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title_divs = soup.find_all('div', class_='title_holder')
    
    albumsWithDesc = []
    for div in title_divs:
        h3 = div.find('h3')
        
        if h3:
            a_tag = h3.find('a')
            if a_tag:
                album = a_tag.get_text(strip=True)
                albumsWithDesc.append(album)
    
    return albumsWithDesc

def main():
    albums = scrape_needle_drop_reviews()
    for album in albums:
        print(album)

if __name__ == "__main__":
    main()
