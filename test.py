import urllib.request

WTT_ICS_URL = "https://wise-tt.com/web/feri/reports?g=582_660_661_662_663_664_665_666&lang=sl&format=ics"

def download_ical(download_path, url=WTT_ICS_URL):
    print(f"Downloading {url}")
    with urllib.request.urlopen(url, timeout=30) as response:
        data = response.read()
    if not data.startswith(b"BEGIN:VCALENDAR"):
        raise ValueError(f"Odgovor z {url} ni ICS datoteka.")
    with open(download_path, "wb") as f:
        f.write(data)
    print(f"Downloaded iCal file to {download_path}")
    return download_path

if __name__ == '__main__':
    download_ical('timetable.ics')
