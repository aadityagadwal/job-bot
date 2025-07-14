# test_system.py
"""
A simple test script to check if the job bot system works end-to-end.
It will:
- Run the main job scraping and application process
- Check if results are saved
- Check if the dashboard API is responsive
"""

import subprocess
import os
import time
import requests
import json
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from notifier.email_notifier import send_email

RESULTS_DIR = "results"
DASHBOARD_URL = "http://127.0.0.1:5000/api/jobs"

def run_main():
    print("[TEST] Running main.py...")
    result = subprocess.run(["python3", "main.py"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("[FAIL] main.py exited with error.")
        print(result.stderr)
        return False
    return True

def check_results():
    print("[TEST] Checking for results files...")
    if not os.path.exists(RESULTS_DIR):
        print(f"[INFO] '{RESULTS_DIR}' directory not found. Creating it now.")
        os.makedirs(RESULTS_DIR, exist_ok=True)
        print(f"[FAIL] No results files found in results/ directory.")
        return False
    files = [f for f in os.listdir(RESULTS_DIR) if f.startswith("found_jobs_")]
    if not files:
        print("[FAIL] No results files found in results/ directory.")
        return False
    print(f"[PASS] Found {len(files)} results file(s).")
    return True

def check_dashboard_api():
    print("[TEST] Checking dashboard API...")
    try:
        resp = requests.get(DASHBOARD_URL, timeout=5)
        if resp.status_code == 200 and isinstance(resp.json(), list):
            print("[PASS] Dashboard API is responsive and returns job data.")
            return True
        else:
            print("[FAIL] Dashboard API did not return expected data.")
            return False
    except Exception as e:
        print(f"[FAIL] Could not connect to dashboard API: {e}")
        return False

def main():
    all_passed = True
    if not run_main():
        all_passed = False
    if not check_results():
        all_passed = False
    print("[INFO] Please ensure the dashboard is running (python dashboard/app.py)")
    time.sleep(2)
    if not check_dashboard_api():
        all_passed = False

    if all_passed:
        print("\n[SUCCESS] System test passed! Your job bot is working end-to-end.")
        # Send test email with stats
        send_test_email()
    else:
        print("\n[FAIL] Some tests failed. Please check the output above.")


def send_test_email():
    # Load config
    config_path = os.path.join("config", "user_config.json")
    if not os.path.exists(config_path):
        print("[WARN] Config file not found, cannot send email.")
        return
    with open(config_path) as f:
        config = json.load(f)
    # Find latest results file
    if not os.path.exists(RESULTS_DIR):
        print("[WARN] No results directory, cannot send email.")
        return
    files = [f for f in os.listdir(RESULTS_DIR) if f.startswith("found_jobs_")]
    if not files:
        print("[WARN] No results file, cannot send email.")
        return
    latest = sorted(files)[-1]
    with open(os.path.join(RESULTS_DIR, latest)) as f:
        jobs = json.load(f)
    total = len(jobs)
    applied = sum(1 for j in jobs if j.get("applied"))
    companies = len(set(j.get("company","") for j in jobs))
    # Compose summary
    subject = "Job Bot System Test: SUCCESS"
    body = f"""
Job Bot System Test PASSED!\n\nJob stats:\n- Total jobs found: {total}\n- Unique companies: {companies}\n- Applied to: {applied} jobs\n\nThis is an automated test email.\n"""
    # Use the same send_email function as main.py
    try:
        send_email(jobs, config, subject=subject, body=body)
        print("[PASS] Test summary email sent.")
    except Exception as e:
        print(f"[FAIL] Could not send test email: {e}")

if __name__ == "__main__":
    main()
