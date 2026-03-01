#!/usr/bin/env python3
"""
Main script to download timetable from Wise-TT and convert it to JSON
"""
from test import download_ical
from icsToJson import parse_ics_to_json
from uploadToFirebase import upload_to_firebase
from datetime import datetime
import os

def main():
    print(f"Run started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # Step 1: Download the .ics file
    print("=" * 60)
    print("Step 1: Downloading timetable from Wise-TT...")
    print("=" * 60)
    
    timetable_config = {
        'schoolcode': 'um_feri',
        'filterId': '0;254;0;0;'
    }
    ics_path = 'timetable.ics'
    
    download_ical(timetable=timetable_config, download_path=ics_path)
    
    # Step 2: Convert .ics to JSON
    print("\n" + "=" * 60)
    print("Step 2: Converting ICS to JSON...")
    print("=" * 60)
    
    json_path = 'school.json'
    parse_ics_to_json(ics_path, json_path)
    
    # Step 3: Upload to Firebase (if configured)
    if os.path.exists('.env'):
        print("\n" + "=" * 60)
        print("Step 3: Uploading to Firebase...")
        print("=" * 60)
        try:
            upload_to_firebase(json_path)
        except Exception as e:
            print(f"⚠ Firebase upload failed: {str(e)}")
            print("Continuing without Firebase upload...")
    else:
        print("\n⚠ No .env file found, skipping Firebase upload")
    
    print("\n" + "=" * 60)
    print("✓ Process completed successfully!")
    print(f"✓ ICS file saved to: {ics_path}")
    print(f"✓ JSON file saved to: {json_path}")
    print("=" * 60)
    print(f"Run finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    main()
