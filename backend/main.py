from fastapi import FastAPI, HTTPException
import os
import json
import firebase_admin
from firebase_admin import credentials, auth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Initialize Firebase Admin SDK
try:
    firebase_credentials_json = os.getenv("FIREBASE_CREDENTIALS")
    if not firebase_credentials_json:
        raise ValueError("FIREBASE_CREDENTIALS environment variable not set.")
    
    cred = credentials.Certificate(json.loads(firebase_credentials_json))
    firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK initialized successfully.")
except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {e}")
    # Depending on deployment, you might want to exit or raise an error here
    # For now, we'll let the app run but log the error.

@app.get("/")
async def root():
    return {"message": "FastAPI Backend is running and Firebase initialized!"}

@app.get("/test-firebase-auth")
async def test_firebase_auth():
    try:
        # Try to list a small number of users to test auth
        # This requires the Firebase Admin SDK to be properly initialized
        users_page = auth.list_users(max_results=1)
        return {"message": "Firebase Auth seems to be working!", "first_user_uid": users_page.users[0].uid if users_page.users else "No users found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firebase Auth test failed: {e}")
