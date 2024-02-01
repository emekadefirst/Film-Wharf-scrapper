# save.py
import asyncio
import os
import pandas as pd
from datetime import datetime
from nkiri import scrape_nkiri_data_async, process_movie_data_async
from update_google_sheets import update_google_sheet

async def save_data_to_csv_and_update_sheet():
    nkiri_url = "https://nkiri.com/category/international/"

    # Scrape data
    movies_data = await scrape_nkiri_data_async(nkiri_url)

    # Process and save data
    current_datetime = datetime.now().strftime("%m%d%y-%H%M")
    csv_filename = f"data{current_datetime}.csv"

    await process_movie_data_async(movies_data)

    # Save data to CSV
    df = pd.DataFrame(movies_data, columns=["Link", "Title", "Image URL"])
    df.to_csv(os.path.join(os.getcwd(), csv_filename), index=False)
    print(f"Data saved to {csv_filename}")

    # Update Google Sheet
    sheet_id = '1sBebAgcrHDLXWse8vo2xqtHaHOblSjm1aLWyd8HKY2U'
    update_google_sheet(sheet_id, csv_filename)

# Run the save_data_to_csv_and_update_sheet function
asyncio.run(save_data_to_csv_and_update_sheet())
