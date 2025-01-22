import os
from firebase_admin import credentials, initialize_app


def initialize_firebase():

    FIREBASE_KEY_PATH = os.getenv("FIREBASE_KEY_PATH", "locateyourself.json")
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    initialize_app(cred, {
        "databaseURL": "https://locateyourself-6e64f-default-rtdb.firebaseio.com/"
    })
print("Firebase initialized.")
print(f"Using Firebase credentials file: {"locateyourself.json"}")
