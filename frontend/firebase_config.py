import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
import os

# IMPORTANT: Replace with your Firebase project's configuration.
# You can get this from the Firebase console.
FIREBASE_CONFIG = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "YOUR_AUTH_DOMAIN",
    "projectId": "YOUR_PROJECT_ID",
    "storageBucket": "YOUR_STORAGE_BUCKET",
    "messagingSenderId": "YOUR_MESSAGING_SENDER_ID",
    "appId": "YOUR_APP_ID",
    "databaseURL": "YOUR_DATABASE_URL"
}

# IMPORTANT: Replace with the path to your Firebase service account key file.
# You can download this from the Firebase console.
# GOOGLE_APPLICATION_CREDENTIALS = "path/to/your/serviceAccountKey.json"

pb = None
auth = None
db = None
FIREBASE_INIT_ERROR = None

try:
    # Check if the app is already initialized
    if not firebase_admin._apps:
        # service_account_key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        # if not service_account_key_path:
        #     raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        
        # cred = credentials.Certificate(service_account_key_path)
        # firebase_admin.initialize_app(cred)
        pass # Bypassing for now as we don't have the service account file

    pb = pyrebase.initialize_app(FIREBASE_CONFIG)
    auth = pb.auth()
    db = pb.database()
except Exception as e:
    FIREBASE_INIT_ERROR = str(e)
