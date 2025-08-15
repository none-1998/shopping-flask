from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Set up Chrome options (optional)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Opens browser full screen
# options.add_argument("--headless")       # Uncomment if you want headless mode

# Create the WebDriver
driver = webdriver.Chrome(options=options)

# Load Excel file
df = pd.read_excel("totalads.xlsx")

# Get list of URLs from the "image_url" column (ignore empty rows)
urls = df["image_url"].dropna().tolist()

srcs = []
for url in urls:
    try:
        print(f"Visiting: {url}")
        driver.get(url)
        time.sleep(5)

        img_tag = driver.find_elements(By.XPATH, "//div[contains(@class, 'imageGallery_imageBorder__JZVXC')]//img")

        if img_tag:
            src = img_tag[0].get_attribute("src")
        else:
            src = None
        srcs.append(src)



    except Exception as e:
        print(f"Error on {url}: {e}")

df["img_src"] = srcs

df.to_excel("totalads.xlsx", index=False, engine="openpyxl")

input("Finished. Press Enter to close the browser...")
driver.quit()
