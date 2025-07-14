# scraper/greenhouse_scraper.py
import requests

def scrape_greenhouse(config):
    all_jobs = []
    search_url = "https://boards-api.greenhouse.io/v1/boards/{board}/jobs"

    # Optional: You can prefetch public boards or keep this configurable
    public_boards = config.get("greenhouse_boards", [])

    for board in public_boards:
        try:
            response = requests.get(search_url.format(board=board))
            jobs = response.json().get("jobs", [])

            for job in jobs:
                title = job.get("title", "").lower()
                location = job.get("location", {}).get("name", "")
                if any(kw.lower() in title for kw in config["keywords"]):
                    if any(loc.lower() in location.lower() for loc in config["locations"]):
                        all_jobs.append({
                            "title": job.get("title"),
                            "company": job.get("company", board),
                            "location": location,
                            "url": job.get("absolute_url"),
                            "source": "Greenhouse"
                        })
        except Exception as e:
            print(f"⚠️ Error scraping Greenhouse board '{board}': {e}")

    print(f"[DEBUG] {len(all_jobs)} jobs found in Greenhouse")
    return all_jobs
