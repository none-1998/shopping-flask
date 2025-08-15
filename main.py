import requests
from bs4 import BeautifulSoup
import pandas as pd

df = pd.read_excel("totalads.xlsx")

urls = []
for index, row in df.iterrows():
    url = row.get("image_url", "")
    urls.append(url)
image_urls = []
for url in urls:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("response")
            soup = BeautifulSoup(response.text, "html.parser")
            picture = soup.find("picture", attrs={"style": "max-width:100%;max-height:280px;margin:0 auto"})
            img = picture.find("img")
            if img and img.get("src"):
                image_urls.append(img["src"])
            else:
                image_urls.append(None)

        else:
            image_urls.append(None)
            print("none added")

    except Exception as e:
        print(f"error scraping {url}: {e}")
        image_urls.append(None)


df["images"] = image_urls

df.to_excel("totalads.xlsx", index=False, engine="openpyxl")

print("done")