import requests
from bs4 import BeautifulSoup
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; LeadGenBot/1.0)"
}

def scrape_yelp_no_website(city="Toronto", state="ON"):
    leads = []
    for offset in range(0, 50, 10):  # 5 pages
        url = f"https://www.yelp.com/search?find_desc=business&find_loc={city}%2C%20{state}&start={offset}"
        resp = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(resp.text, 'html.parser')
        listings = soup.select("div.container__09f24__21w3G")

        for biz in listings:
            try:
                name_tag = biz.select_one("a.css-19v1rkv")
                if not name_tag:
                    continue
                name = name_tag.text.strip()
                source_url = "https://www.yelp.com" + name_tag["href"]
                website_link = biz.select_one("a[href*='biz_redir']")
                if website_link:
                    continue  # Skip businesses with websites

                location = biz.select_one("address").text.strip() if biz.select_one("address") else f"{city}, {state}"
                leads.append({
                    "business_name": name,
                    "location": location,
                    "email": "N/A",
                    "source_url": source_url
                })
            except Exception:
                continue
        time.sleep(2)
    return leads

def scrape_businesses_without_websites():
    cities = [("New York", "NY"), ("Toronto", "ON"), ("Chicago", "IL")]
    all_leads = []
    for city, state in cities:
        leads = scrape_yelp_no_website(city, state)
        all_leads.extend(leads)
    return all_leads
