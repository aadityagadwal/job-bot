# Clean imports and sys.path
import os
import sys
import json
import requests
import subprocess
import importlib
from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scraper.remoteok_scraper import scrape_remoteok

app = Flask(__name__)

# --- PUBLIC JOB API ENDPOINTS ---
@app.route('/api/public-jobs/remoteok')
def api_public_jobs_remoteok():
    try:
        resp = requests.get('https://remoteok.com/api', timeout=10)
        jobs = resp.json()
        if jobs and isinstance(jobs, list) and isinstance(jobs[0], dict) and 'id' not in jobs[0]:
            jobs = jobs[1:]
        return jsonify({'success': True, 'jobs': jobs})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'jobs': []})

@app.route('/api/public-jobs/arbeitnow')
def api_public_jobs_arbeitnow():
    try:
        resp = requests.get('https://www.arbeitnow.com/api/job-board-api', timeout=10)
        data = resp.json()
        jobs = data.get('data', [])
        return jsonify({'success': True, 'jobs': jobs})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'jobs': []})

# --- API STATUS ENDPOINT ---
@app.route('/api/status')
def api_status():
    status = {}
    endpoints = [
        ('/api/jobs', 'jobs'),
        ('/api/find-jobs', 'find_jobs'),
        ('/api/test-system', 'test_system'),
        ('/api/scrape-remoteok', 'scrape_remoteok'),
        ('/api/public-jobs/remoteok', 'public_remoteok'),
        ('/api/public-jobs/arbeitnow', 'public_arbeitnow'),
    ]
    for ep, name in endpoints:
        try:
            url = f"http://127.0.0.1:5000{ep}"
            if ep in ['/api/find-jobs', '/api/test-system', '/api/scrape-remoteok']:
                resp = requests.post(url, timeout=3)
            else:
                resp = requests.get(url, timeout=3)
            status[name] = resp.status_code == 200
        except Exception:
            status[name] = False
    try:
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config/user_config.json'))
        with open(config_path) as f:
            config = json.load(f)
        email_cfg = config.get('email', {})
        status['email_configured'] = bool(email_cfg.get('enabled') and email_cfg.get('smtp_user') and email_cfg.get('smtp_password') and email_cfg.get('recipient'))
    except Exception:
        status['email_configured'] = False
    return jsonify(status)

# --- SCRAPER STATUS ENDPOINT ---
@app.route('/api/scraper-status')
def api_scraper_status():
    scrapers = [
        ("Indeed", "scraper.indeed_scraper", "scrape_indeed"),
        ("Greenhouse", "scraper.greenhouse_scraper", "scrape_greenhouse"),
        ("Lever", "scraper.lever_scraper", "scrape_lever"),
        ("Jobright.ai", "scraper.jobright_scraper", "scrape_jobright"),
        ("MigrateMate", "scraper.migratemate_scraper", "scrape_migratemate"),
        ("LinkedIn", "scraper.linkedin_scraper", "scrape_linkedin"),
        ("Workday", "scraper.workday_scraper", "scrape_workday"),
        ("RemoteOK", "scraper.remoteok_scraper", "scrape_remoteok"),
    ]
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config/user_config.json'))
    with open(config_path) as f:
        config = json.load(f)
    status = []
    for name, mod_path, func_name in scrapers:
        try:
            mod = importlib.import_module(mod_path)
            func = getattr(mod, func_name)
            jobs = func(config)
            status.append({"name": name, "status": True, "count": len(jobs)})
        except Exception as e:
            status.append({"name": name, "status": False, "error": str(e)})
    return jsonify(status)


# POST endpoint for dashboard button: returns jobs and debug info
@app.route('/api/scrape-remoteok', methods=['POST'])
def api_scrape_remoteok():
    try:
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config/user_config.json'))
        with open(config_path) as f:
            config = json.load(f)
        jobs = scrape_remoteok(config)
        return jsonify({'success': True, 'jobs': jobs})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'jobs': []})