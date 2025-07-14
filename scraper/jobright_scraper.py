# scraper/jobright_scraper.py
import requests


def scrape_jobright(config):
    all_jobs = []
    base_url = "https://api.jobright.ai/jobs"

    try:
        response = requests.get(base_url)
        jobs = response.json().get("results", [])

        for job in jobs:
            title = job.get("title", "").lower()
            location = job.get("location", "")

            if any(kw.lower() in title for kw in config["keywords"]):
                if any(loc.lower() in location.lower() for loc in config["locations"]):
                    all_jobs.append({
                        "title": job.get("title"),
                        "company": job.get("company"),
                        "location": location,
                        "url": job.get("url"),
                        "source": "Jobright.ai"
                    })
    except Exception as e:
        print(f"⚠️ Error scraping Jobright.ai: {e}")

    print(f"[DEBUG] {len(all_jobs)} jobs found in Jobright.ai")
    return all_jobs
