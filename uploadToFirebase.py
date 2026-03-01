#!/usr/bin/env python3
"""
Upload school.json data to Firebase Realtime Database
"""
import json
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, db

def upload_to_firebase(json_file_path='school.json', db_path=''):
    """
    Upload JSON data to Firebase Realtime Database
    
    Args:
        json_file_path: Path to the JSON file to upload
        db_path: Database path where data will be stored (empty string for root)
    """
    # Load environment variables
    load_dotenv()
    
    # Get Firebase configuration from environment
    database_url = os.getenv('FIREBASE_DATABASE_URL')
    service_account_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH')
    
    if not database_url:
        raise ValueError("FIREBASE_DATABASE_URL not found in .env file")
    
    if not service_account_path:
        raise ValueError("FIREBASE_SERVICE_ACCOUNT_PATH not found in .env file")
    
    if not os.path.exists(service_account_path):
        raise ValueError(f"Service account file not found: {service_account_path}")
    
    print("=" * 60)
    print("Initializing Firebase connection...")
    print("=" * 60)
    
    # Initialize Firebase Admin SDK with service account credentials
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': database_url
    })
    print(f"✓ Authenticated using service account: {service_account_path}")
    
    # Read JSON data
    print(f"\nReading data from {json_file_path}...")
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    new_hash = data.get('Hash')
    classes_count = len(data.get('Classes', []))
    
    print(f"✓ Loaded {classes_count} classes")
    print(f"✓ New data hash: {new_hash}")
    
    # Get reference to database root or specified path
    ref = db.reference(db_path) if db_path else db.reference()
    
    # Check if hash has changed
    print(f"\nChecking for changes...")
    existing_hash = ref.child('Hash').get()
    
    if existing_hash == new_hash:
        print("\n" + "=" * 60)
        print("⏭️  No changes detected - Hash is the same")
        print(f"   Current hash: {existing_hash}")
        print("   Skipping upload to Firebase")
        print("=" * 60)
        return False
    
    print(f"✓ Changes detected!")
    print(f"  Old hash: {existing_hash or 'None (first upload)'}")
    print(f"  New hash: {new_hash}")
    
    # Upload Hash and Classes separately to root level
    print(f"\nUploading data to Firebase at root level...")
    ref.child('Hash').set(new_hash)
    ref.child('Classes').set(data.get('Classes'))
    
    print("\n" + "=" * 60)
    print("✓ Successfully uploaded to Firebase Realtime Database!")
    print(f"✓ Database URL: {database_url}")
    print(f"✓ Structure: /Hash and /Classes at root level")
    print(f"✓ Classes uploaded: {classes_count}")
    print("=" * 60)
    
    print("\n" + "=" * 60)
    print("✓ Successfully uploaded to Firebase Realtime Database!")
    print(f"✓ Database URL: {database_url}")
    print(f"✓ Path: /{db_path}/")
    print(f"✓ Classes uploaded: {len(data.get('Classes', []))}")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    try:
        upload_to_firebase()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise
