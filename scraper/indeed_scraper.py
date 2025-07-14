# scraper/indeed_scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_indeed(config):
    base_url = "https://www.indeed.com/jobs"
    all_jobs = []

    for keyword in config['keywords']:
        for location in config['locations']:
            params = {
                "q": keyword,
                "l": location,
                "radius": 25,
                "limit": 10,
            }
            print(f"🔎 Searching Indeed for '{keyword}' in '{location}'")
            response = requests.get(base_url, params=params)
            soup = BeautifulSoup(response.text, "html.parser")

            for div in soup.find_all("div", class_="job_seen_beacon"):
                title_elem = div.find("h2")
                if title_elem:
                    job = {
                        "title": title_elem.text.strip(),
                        "company": div.find("span", class_="companyName").text.strip() if div.find("span", class_="companyName") else "",
                        "location": location,
                        "url": "https://www.indeed.com" + title_elem.find("a")['href'] if title_elem.find("a") else "",
                        "source": "Indeed"
                    }
                    all_jobs.append(job)

    print(f"[DEBUG] {len(all_jobs)} jobs found in Indeed")
    return all_jobs
