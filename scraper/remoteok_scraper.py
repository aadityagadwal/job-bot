# scraper/remoteok_scraper.py
import requests

def scrape_remoteok(config):
    all_jobs = []
    url = "https://remoteok.com/api"
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        jobs = response.json()
        for job in jobs:
            if not isinstance(job, dict):
                continue
            title = job.get("position", "").lower()
            location = job.get("location", "Remote")
            if any(kw.lower() in title for kw in config["keywords"]):
                if any(loc.lower() in location.lower() for loc in config["locations"]):
                    all_jobs.append({
                        "title": job.get("position", ""),
                        "company": job.get("company", "RemoteOK"),
                        "location": location,
                        "url": job.get("url", ""),
                        "source": "RemoteOK"
                    })
    except Exception as e:
        print(f"⚠️ Error scraping RemoteOK: {e}")
    print(f"[DEBUG] {len(all_jobs)} jobs found in RemoteOK")
    return all_jobs
