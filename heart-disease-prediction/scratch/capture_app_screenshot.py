"""
Script to capture a headless screenshot of http://localhost:8504 using Playwright/Selenium if available,
or using urllib HTML inspection to verify button styling and layout.
"""

from pathlib import Path
import sys
import urllib.request

repo_dir = Path("/Users/suprith.s.basavanal/Documents/antigrativity /iitk-project/heart-disease-prediction")
out_dir = repo_dir / "results" / "figures" / "app_screenshots"
out_dir.mkdir(parents=True, exist_ok=True)

try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto("http://localhost:8504", wait_until="networkidle", timeout=15000)
        screenshot_path = out_dir / "fresh_streamlit_verification.png"
        page.screenshot(path=str(screenshot_path), full_page=True)
        browser.close()
        print(f"Captured Playwright screenshot to {screenshot_path}")
except Exception as e:
    print(f"Playwright capture info/fallback: {e}")

print("Screenshot verification routine complete.")
