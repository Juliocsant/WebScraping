from playwright.sync_api import sync_playwright


def scrape_page(url):
     with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()
                page.goto(url)
                html = page.content()
                browser.close()
                return html
           