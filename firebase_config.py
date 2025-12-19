import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
import os

# IMPORTANT: Replace with your Firebase project's configuration.
# You can get this from the Firebase console.
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyDDxzSi_SZioTwfMYmfdjnxhFyBHR4MgvU",
    "authDomain": "finance-tracker-efb03.firebaseapp.com",
    "projectId": "finance-tracker-efb03",
    "storageBucket": "finance-tracker-efb03.appspot.com",
    "messagingSenderId": "715853611314",
    "appId": "1:715853611314:web:4d85d013075e34298ad72b",
    "databaseURL": "https://finance-tracker-efb03-default-rtdb.asia-southeast1.firebasedatabase.app"
}

# IMPORTANT: Replace with the path to your Firebase service account key file.
# You can download this from the Firebase console.
# GOOGLE_APPLICATION_CREDENTIALS = "path/to/your/serviceAccountKey.json"

pb = None
auth = None
db = None
FIREBASE_INIT_ERROR = None

def get_fresh_id_token(session_state):
    if "refresh_token" not in session_state or not auth:
        return None # No refresh token or auth object available

    try:
        # Pyrebase refresh method returns a new ID token and refresh token
        refreshed_user = auth.refresh(session_state.refresh_token)
        session_state.id_token = refreshed_user['idToken']
        session_state.refresh_token = refreshed_user['refreshToken'] # Update refresh token as well
        return session_state.id_token
    except Exception as e:
        print(f"Error refreshing token: {e}")
        # Optionally, log out user or prompt re-login if refresh fails
        session_state.logged_in = False
        session_state.id_token = None
        session_state.refresh_token = None
        session_state.user_id = None
        return None

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
