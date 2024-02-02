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

url = 'https://filmwharf.vercel.app/add.html'
driver.get(url)

time.sleep(10)
file_path = 'data020224-1211.csv'
df = pd.read_csv(file_path)

for _, row in df.iterrows():
    # Scroll down to make the form visible
    actions = ActionChains(driver)
    actions.send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(2)

    # Fill the form with data from the CSV file
    driver.find_element(By.NAME, 'name').send_keys(row['Title'])
    driver.find_element(By.NAME, 'genre').send_keys("base")
    current_date = datetime.now().strftime('%Y-%m-%d')
    driver.find_element(By.NAME, 'release_date').send_keys(current_date)
    driver.find_element(By.NAME, 'download_link').send_keys(row['Link'])
    driver.find_element(By.NAME, 'thumbnail_url').send_keys(row['Image URL'])
    driver.find_element(By.NAME, 'source').send_keys("Nkiri")

    # Submit the form
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-primary'))).click()

    # Wait for a short time to avoid being rate-limited by the website
    time.sleep(2)

driver.quit()
