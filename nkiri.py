import pandas as pd
import asyncio
import aiohttp
import backoff
from bs4 import BeautifulSoup
from tqdm import tqdm

async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()

@backoff.on_exception(backoff.expo, aiohttp.ClientError, max_tries=1)
async def scrape_nkiri_data_async(url, num_pages=4):
    movies_data = []

    async with aiohttp.ClientSession() as session:
        tasks = []

        for num in range(1, num_pages + 1):
            page_url = f"{url}/page/{num}"
            tasks.append(fetch_page(session, page_url))

        pages = await asyncio.gather(*tasks)

        for page_content in tqdm(pages, desc="Pages Scraped"):
            soup = BeautifulSoup(page_content, "html.parser")
            movies = soup.find_all("div", class_="blog-entry-inner")

            for movie in tqdm(movies, desc="Entries Scraped", leave=False):
                link_element = movie.find('a')
                link = link_element.get('href')

                title_element = movie.find('h2', class_='blog-entry-title entry-title')
                title = title_element.text.strip() if title_element else "N/A"

                image_element = movie.find('img', class_='attachment-full size-full wp-post-image')
                image_url = image_element.get('src') if image_element else "N/A"

                movies_data.append((link, title, image_url))

    return movies_data

@backoff.on_exception(backoff.expo, aiohttp.ClientError, max_tries=5)
async def nkiri_data_async(session, link, title, image_url):
    async with session.get(link) as response:
        page_content = await response.text()

    soup = BeautifulSoup(page_content, "html.parser")
    data_block = soup.find('div', {'data-id': '3f2169e'})

    if data_block:
        download_link_element = data_block.find('a', class_='elementor-button elementor-button-link elementor-size-md')
        download_link = download_link_element.get('href') if download_link_element else None
        return {'Link': link, 'Title': title, 'Image URL': image_url, 'Download Link': download_link}
    else:
        print(f"Data block with data-id '3f2169e' not found for link: {link}")
        # Return None for entries where data is not found
        return None

async def process_movie_data_async(movies_data):
    async with aiohttp.ClientSession() as session:
        tasks = [nkiri_data_async(session, link, title, image_url) for link, title, image_url in movies_data]
        # Filter out entries where any of the required fields is not found
        return [entry for entry in await asyncio.gather(*tasks) if entry is not None]

# Example usage
nkiri_url = "https://nkiri.com/category/international/"
movies_data = asyncio.run(scrape_nkiri_data_async(nkiri_url))
processed_data = asyncio.run(process_movie_data_async(movies_data))

# Convert the processed data to a Pandas DataFrame
df = pd.DataFrame(processed_data)

# Save the DataFrame to a CSV file
df.to_csv('nkiri_movies_data.csv', index=False)

print("CSV file saved successfully.")
