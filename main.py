# main.py
from scraper.indeed_scraper import scrape_indeed
from scraper.greenhouse_scraper import scrape_greenhouse
from scraper.lever_scraper import scrape_lever
from scraper.jobright_scraper import scrape_jobright
from scraper.migratemate_scraper import scrape_migratemate
from scraper.linkedin_scraper import scrape_linkedin
from scraper.workday_scraper import scrape_workday
from apply.auto_apply import auto_apply_to_job
from notifier.email_notifier import send_email
from datetime import datetime
import json
import os

CONFIG_PATH = 'config/user_config.json'

# Load user config

def load_config():
    if not os.path.exists(CONFIG_PATH):
        # Create default config if missing
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        default_config = {
            "email": {"enabled": False},
            "keywords": ["engineer", "developer"],
            "location": "Remote",
            "locations": ["Remote"]
        }
        with open(CONFIG_PATH, 'w') as f:
            json.dump(default_config, f, indent=2)
        print(f"[INFO] Created default config at {CONFIG_PATH}. Please edit it as needed.")
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    # Ensure 'locations' key is present
    if 'locations' not in config:
        loc = config.get('location', 'Remote')
        config['locations'] = [loc] if isinstance(loc, str) else loc
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"[INFO] Added missing 'locations' key to config at {CONFIG_PATH}.")
    return config

def save_job_data(jobs, applied_jobs):
    now = datetime.now().strftime("%Y-%m-%d")
    job_data = []
    for job in jobs:
        job_data.append({
            "title": job.get("title", ""),
            "company": job.get("company", ""),
            "location": job.get("location", ""),
            "applied": job in applied_jobs,
            "date_found": now
        })
    os.makedirs("results", exist_ok=True)
    with open(f"results/found_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
        json.dump(job_data, f, indent=2)

def main():
    config = load_config()
    print(f"[DEBUG] Loaded config from {CONFIG_PATH}:")
    print(json.dumps(config, indent=2))
    all_jobs = []

    print("🔍 Scraping Indeed...")
    all_jobs += scrape_indeed(config)

    print("🔍 Scraping Greenhouse...")
    all_jobs += scrape_greenhouse(config)

    print("🔍 Scraping Lever...")
    all_jobs += scrape_lever(config)

    print("🔍 Scraping Jobright.ai...")
    all_jobs += scrape_jobright(config)

    print("🔍 Scraping MigrateMate...")
    all_jobs += scrape_migratemate(config)

    print("🔍 Scraping LinkedIn...")
    all_jobs += scrape_linkedin(config)

    print("🔍 Scraping Workday...")
    all_jobs += scrape_workday(config)

    print(f"✅ Total Jobs Found: {len(all_jobs)}")

    applied_jobs = []
    for job in all_jobs:
        success = auto_apply_to_job(job, config)
        if success:
            applied_jobs.append(job)

    print(f"📩 Applied to {len(applied_jobs)} jobs.")

    if config.get("email", {}).get("enabled"):
        send_email(applied_jobs, config)

    save_job_data(all_jobs, applied_jobs)

if __name__ == '__main__':
    main()
