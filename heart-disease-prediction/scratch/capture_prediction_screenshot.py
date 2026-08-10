"""
Script to capture prediction card screenshot of http://localhost:8504 using Playwright.
"""

from pathlib import Path
from playwright.sync_api import sync_playwright

repo_dir = Path("/Users/suprith.s.basavanal/Documents/antigrativity /iitk-project/heart-disease-prediction")
out_dir = repo_dir / "results" / "figures" / "app_screenshots"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 1100})
    page.goto("http://localhost:8504", wait_until="networkidle", timeout=15000)
    
    # Click Predict button
    page.get_by_role("button", name="Predict Heart Disease Risk").click()
    page.wait_for_timeout(2000)
    
    screenshot_path = out_dir / "fresh_prediction_result_verification.png"
    page.screenshot(path=str(screenshot_path), full_page=True)
    browser.close()

print(f"Captured prediction result screenshot to {screenshot_path}")
