import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def scrape_nkiri_data(url, num_pages=73):
    movies_data = []

    for num in tqdm(range(1, num_pages + 1), desc="Pages Scraped"):
        page_url = f"{url}/page/{num}"
        res = requests.get(page_url)
        soup = BeautifulSoup(res.content, "html.parser")

        movies = soup.find_all("div", class_="blog-entry-inner")

        for movie in tqdm(movies, desc="Entries Scraped", leave=False):
            link_element = movie.find('a')
            link = link_element.get('href')
            
            title_element = movie.find('h2', class_='blog-entry-title entry-title')
            title = title_element.text.strip() if title_element else "N/A"
            
            image_element = movie.find('img', class_='attachment-full size-full wp-post-image')
            image_url = image_element.get('src') if image_element else "N/A"
            
            # Append movie data to the list
            movies_data.append((link, title, image_url))

    return movies_data

def process_movie_data(movie_data):
    for link, title, image_url in movie_data:
        nkiri_data(link, title, image_url)

def nkiri_data(link, title, image_url):
    res = requests.get(link)
    soup = BeautifulSoup(res.content, "html.parser")

    data_block = soup.find('div', {'data-id': '3f2169e'})

    if data_block:
        download_link_element = data_block.find('a', class_='elementor-button elementor-button-link elementor-size-md')
        download_link = download_link_element.get('href') if download_link_element else None
        print(link)
        print(title)
        print(image_url)
        print(download_link)
    else:
        print("Data block with data-id '3f2169e' not found.")

# Example usage
nkiri_url = "https://nkiri.com/category/international/"
movies_data = scrape_nkiri_data(nkiri_url)
process_movie_data(movies_data)
processed_data = [entry for entry in process_movie_data if entry is not None]

# Convert the processed data to a Pandas DataFrame
df = pd.DataFrame(processed_data)

# Save the DataFrame to a CSV file
df.to_csv('nkiri_movies_data.csv', index=False)

print("CSV file saved successfully.")
