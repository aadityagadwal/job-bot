# scraper/linkedin_scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep


def scrape_linkedin(config):
    all_jobs = []
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    try:
        driver = webdriver.Chrome(options=chrome_options)

        for keyword in config["keywords"]:
            for location in config["locations"]:
                search_url = f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '%20')}&location={location.replace(' ', '%20')}&f_TPR=r86400"
                print(f"🌐 LinkedIn: {keyword} in {location}")
                driver.get(search_url)
                sleep(5)  # Wait for dynamic content to load

                job_cards = driver.find_elements(By.CLASS_NAME, "base-card")

                for card in job_cards[:10]:
                    try:
                        title = card.find_element(By.CLASS_NAME, "base-search-card__title").text.strip()
                        company = card.find_element(By.CLASS_NAME, "base-search-card__subtitle").text.strip()
                        loc = card.find_element(By.CLASS_NAME, "job-search-card__location").text.strip()
                        url = card.find_element(By.TAG_NAME, "a").get_attribute("href")

                        all_jobs.append({
                            "title": title,
                            "company": company,
                            "location": loc,
                            "url": url,
                            "source": "LinkedIn"
                        })
                    except Exception as e:
                        print(f"⚠️ Error parsing a LinkedIn job card: {e}")

        driver.quit()
    except Exception as e:
        print(f"⚠️ LinkedIn scraping error: {e}")

    print(f"[DEBUG] {len(all_jobs)} jobs found in LinkedIn")
    return all_jobs
