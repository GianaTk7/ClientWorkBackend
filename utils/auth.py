import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, status
import os
import json

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    try:
        # Try to load from environment variable first
        firebase_creds = os.getenv("FIREBASE_CREDENTIALS")
        if firebase_creds:
            cred_dict = json.loads(firebase_creds)
            cred = credentials.Certificate(cred_dict)
        else:
            # Try to load from file
            cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase-service-account.json")
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
            else:
                print("Warning: No Firebase credentials found. Auth will not work.")
                cred = None
        
        if cred:
            firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Firebase initialization warning: {e}")

async def verify_token(token: str):
    """Verify Firebase ID token"""
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )