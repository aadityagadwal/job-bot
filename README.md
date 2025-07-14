# 📊 Finance Job Bot

A fully automated Python bot that scrapes finance-related job listings from multiple job boards and auto-applies using a given resume. Designed for Valuation, Market Research, M\&A, and other finance analyst roles in the U.S.

---

## 🚀 Features

* 🔍 Scrapes job listings based on roles & locations (not companies)
* 🌎 Focused on U.S. cities (NYC, SF, Washington DC, etc.)
* 🤖 Auto-applies using a placeholder logic (can be extended to Selenium)
* 📬 Sends styled email notifications after successful applications
* 🧾 Logs & saves all jobs found and applied with timestamps
* ⚙️ Runs automatically via GitHub Actions (twice daily)

---

## 🛠️ Installation

```bash
git clone https://github.com/yourusername/finance-job-bot.git
cd finance-job-bot
pip install -r requirements.txt
```

---

## 🔧 Configuration

Edit `config/user_config.json`:

```json
{
  "keywords": ["valuation analyst", "equity research analyst"],
  "locations": ["New York", "Remote", "Washington DC"],
  "resume_path": "resume/sample_resume.pdf",

  "email": {
    "enabled": true,
    "smtp_user": "you@gmail.com",
    "smtp_password": "your_app_password",
    "recipient": ["you@gmail.com", "friend@example.com"]
  },

  "greenhouse_boards": [],
  "lever_boards": [],
  "workday_urls": []
}
```

---

## 🧪 Run Locally

```bash
python main.py
```

Results will be saved under `/results` and logs under `/logs`.

---

## 🕐 GitHub Actions (Automation)

The bot is set to run **twice a day** using `.github/workflows/jobbot.yml`.

```yaml
schedule:
  - cron: '0 9,18 * * *'  # Runs at 9 AM and 6 PM UTC
```

You can trigger manually via GitHub’s **Actions tab > Run workflow**.

---

## 📂 Folder Structure

```
├── apply/
│   └── auto_apply.py
├── config/
│   └── user_config.json
├── logs/
│   └── jobbot.log
├── notifier/
│   └── email_notifier.py
├── results/
├── scraper/
│   ├── greenhouse_scraper.py
│   ├── lever_scraper.py
│   ├── linkedin_scraper.py
│   ├── migratemate_scraper.py
│   ├── jobright_scraper.py
│   └── workday_scraper.py
├── main.py
├── requirements.txt
└── .github/workflows/jobbot.yml
```

---

## 📌 TODO / Extensibility

* Replace placeholder `auto_apply` logic with real form-filling (via Selenium)
* Add Slack/Discord alerts
* Build dynamic board discovery from Greenhouse/Lever APIs
* Add `.env` support for secrets

---

## 🧠 Built With

* Python 3.11
* Selenium
* Requests + BeautifulSoup
* GitHub Actions (CI/CD)

---

## 📫 Contact

Made by Aaditya G ✨ — Contributions welcome!

> Fork this project if you're helping someone land their dream job in finance!
