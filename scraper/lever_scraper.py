# scraper/lever_scraper.py
import requests

def scrape_lever(config):
    all_jobs = []
    lever_boards = config.get("lever_boards", [])

    for board in lever_boards:
        url = f"https://jobs.lever.co/v0/postings/{board}?mode=json"
        try:
            response = requests.get(url)
            postings = response.json()

            for job in postings:
                title = job.get("text", "").lower()
                location = job.get("categories", {}).get("location", "")
                if any(kw.lower() in title for kw in config["keywords"]):
                    if any(loc.lower() in location.lower() for loc in config["locations"]):
                        all_jobs.append({
                            "title": job.get("text"),
                            "company": board,
                            "location": location,
                            "url": job.get("hostedUrl"),
                            "source": "Lever"
                        })
        except Exception as e:
            print(f"⚠️ Error scraping Lever board '{board}': {e}")

    print(f"[DEBUG] {len(all_jobs)} jobs found in Lever")
    return all_jobs
