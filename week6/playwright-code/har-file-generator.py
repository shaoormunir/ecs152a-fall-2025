from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(record_har_path="test.har", ignore_https_errors=True)

    page = context.new_page()
    page.goto("https://ucdavis.edu")

    context.close()
    browser.close()
