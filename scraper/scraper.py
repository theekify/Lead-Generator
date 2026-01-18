import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_LIST_URL = "https://scrapeme.live/shop/page/{}/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

leads = []

def scrape_product_page(url):
    r = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    sku_tag = soup.select_one("span.sku")
    sku = sku_tag.get_text(strip=True) if sku_tag else ""

    return sku


for page in range(1, 6):  # scrape 5 pages
    print(f"Scraping listing page {page}...")
    list_url = BASE_LIST_URL.format(page)

    response = requests.get(list_url, headers=HEADERS, timeout=10)
    if response.status_code != 200:
        print("Failed to load page")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.select("li.product")

    print(f"Found {len(products)} listings")

    for product in products:
        try:
            name = product.select_one("h2").get_text(strip=True)
            price = product.select_one("span.woocommerce-Price-amount").get_text(strip=True)
            url = product.select_one("a")["href"]

            sku = scrape_product_page(url)

            leads.append({
                "lead_name": name,
                "identifier": sku,
                "price_meta": price,
                "profile_url": url
            })

            time.sleep(0.5)

        except Exception:
            continue

    time.sleep(1)

df = pd.DataFrame(leads)
df.to_csv("../data/leads.csv", index=False)

print("DONE. Leads saved to data/leads.csv")
