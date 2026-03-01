from playwright.sync_api import sync_playwright
import hashlib
import datetime
import base64

WTT_API_URL = "https://www.wise-tt.com"

def download_ical(timetable, download_path):
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        url = f"{WTT_API_URL}/wtt_{timetable['schoolcode']}/index.jsp?filterId={timetable['filterId']}"
        response = page.goto(url)
        if not response or not response.ok:
            raise ValueError(f"Napaka pri nalaganju {url}, status: {response.status if response else 'no response'}")
        if page.locator('a[title="Izvoz celotnega urnika v ICS formatu  "]').count() == 0:
            raise ValueError(f"Urnik na {url} nima aktivnih terminov.")
        print(f"Navigated to {url}")
        page.click('a[title="Izvoz celotnega urnika v ICS formatu  "]', timeout=3000)
        print("Clicked on iCal export link")
        with page.expect_download(timeout=5000) as download_info:
            pass  # The click already initiated the download
            print("Waiting for download to start...")
        download = download_info.value
        download.save_as(download_path)
        print(f"Downloaded iCal file to {download_path}")
        browser.close()
    return download_path    

download_ical(
    timetable={'schoolcode': 'um_feri', 'filterId': '0;254;0;0;'},
    download_path='timetable.ics'
    )