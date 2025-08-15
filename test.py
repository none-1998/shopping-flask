import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # Import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os


df = pd.read_excel("totalads.xlsx")

urls = df["image_url"].dropna().to_list()


driver_path = "C:/chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service)  # Pass options to the webdriver


# Function to scrape details of a single product, including the title
def scrape_products(url, product_id):
    print(f"Scraping product {product_id} from {url}")  # Debugging line
    driver.get(url)
    time.sleep(3)

    product_data = {}

    try:

        # image = driver.find_element(By.CLASS_NAME, "div.imageGallery_imageBorder__JZVXC")
        # picture_tag = image.find_element(By.TAG_NAME, "picture")
        # img_tag = picture_tag.find_element(By.TAG_NAME, "img")
        # product_data["تصویر"] = img_tag.get_attribute("src")

        title_element = driver.find_element(By.CSS_SELECTOR, "div.Showcase_name__hrttI")  # Update with correct selector
        text_tag = title_element.find_element(By.TAG_NAME, "h1")
        product_data['نام'] = text_tag.text.strip()

        price_element = driver.find_element(By.CLASS_NAME, "Showcase_buy_box_text__otYW_.Showcase_ellipsis__FxqVh")
        product_data["قیمت"] = price_element.text.strip()

        # Extracting other product details
        detail_titles = driver.find_elements(By.CSS_SELECTOR, "div.jsx-d9bfdb7eefd5a6bf.detail-title")
        detail_values = driver.find_elements(By.CSS_SELECTOR, "div.jsx-d9bfdb7eefd5a6bf.detail-value")

        for title, value in zip(detail_titles, detail_values):
            title_text = title.text.strip()
            value_text = value.text.strip()
            if title_text and value_text:
                product_data[title_text] = value_text

    except Exception as e:
        print(f"Error while scraping details for product {product_id}: {e}")

    # Save each product's data to its own JSON file
    filename = f"product_{product_id}.json"
    with open(filename, "w", encoding="utf_8") as f:
        json.dump(product_data, f, ensure_ascii=False, indent=4)

# Loop through all product links and save each product's details in its own file
for index, url in enumerate(urls):
    scrape_products(url, index + 1)

driver.quit()