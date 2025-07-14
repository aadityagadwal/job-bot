# scraper/migratemate_scraper.py
import requests
from bs4 import BeautifulSoup


def scrape_migratemate(config):
    all_jobs = []
    base_url = "https://migratemate.co/jobs"

    try:
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, "html.parser")

        job_cards = soup.find_all("div", class_="job-card")
        for card in job_cards:
            title_elem = card.find("h2")
            location_elem = card.find("span", class_="job-location")

            if not title_elem:
                continue

            title = title_elem.text.strip().lower()
            location = location_elem.text.strip() if location_elem else "Remote"

            if any(kw.lower() in title for kw in config["keywords"]):
                if any(loc.lower() in location.lower() for loc in config["locations"]):
                    job = {
                        "title": title_elem.text.strip(),
                        "company": "MigrateMate",
                        "location": location,
                        "url": card.find("a")["href"] if card.find("a") else base_url,
                        "source": "MigrateMate"
                    }
                    all_jobs.append(job)
    except Exception as e:
        print(f"⚠️ Error scraping MigrateMate.co: {e}")

    print(f"[DEBUG] {len(all_jobs)} jobs found in MigrateMate")
    return all_jobs
