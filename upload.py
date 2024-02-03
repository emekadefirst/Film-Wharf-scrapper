import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver_path = 'msedgedriver.exe'
driver = webdriver.Edge(executable_path=driver_path)

# Maximize the browser window
driver.maximize_window()

url = 'https://filmwharf.vercel.app/'
driver.get(url)

# Wait for the "Add Movies +" link to be clickable
add_movies_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.LINK_TEXT, 'Add Movies +'))
)
add_movies_button.click()

time.sleep(5)
file_path = 'nkiri_movies_data.csv'
df = pd.read_csv(file_path)

for _, row in df.iterrows():
    # Scroll down to make the form visible
    actions = ActionChains(driver)
    actions.send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(2)  # Adjust sleep time if needed

    # Fill the form with data from the CSV file
    driver.find_element(By.NAME, 'name').send_keys(row['Title'])
    driver.find_element(By.NAME, 'genre').send_keys(row['Genres'])
    current_date = datetime.now().strftime('%d-%m-%Y')
    driver.find_element(By.NAME, 'release_date').send_keys(current_date)
    driver.find_element(By.NAME, 'download_link').send_keys(row['Download Link'])
    driver.find_element(By.NAME, 'thumbnail_url').send_keys(row['Image URL'])
    enter = driver.find_element(By.NAME, 'source')
    enter.send_keys("Nkiri")
    enter.send_keys(Keys.ENTER)
    time.sleep(2)  # Adjust sleep time if needed

driver.quit()
