# scraper/workday_scraper.py
import requests
import json


def scrape_workday(config):
    all_jobs = []
    workday_urls = config.get("workday_urls", [])

    for url in workday_urls:
        try:
            response = requests.get(url)
            data = response.json()
            for job in data.get("jobPostings", []):
                title = job.get("title", "").lower()
                location = job.get("locationsText", "")
                if any(kw.lower() in title for kw in config["keywords"]):
                    if any(loc.lower() in location.lower() for loc in config["locations"]):
                        all_jobs.append({
                            "title": job.get("title"),
                            "company": job.get("companyName", "Workday Company"),
                            "location": location,
                            "url": job.get("externalPath", ""),
                            "source": "Workday"
                        })
        except Exception as e:
            print(f"⚠️ Error scraping Workday URL '{url}': {e}")

    print(f"[DEBUG] {len(all_jobs)} jobs found in Workday")
    return all_jobs