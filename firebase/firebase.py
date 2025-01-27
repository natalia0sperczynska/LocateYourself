import os
from firebase_admin import credentials, initialize_app


def initialize_firebase():
    """
    Initializes the Firebase application with the credentials provided in the environment variable or default to 'locateyourself.json'.
    The Firebase Realtime Database URL is configured to the 'locateyourself-6e64f-default-rtdb' instance.

    This function should be called at the start of the application to set up Firebase.

    The credentials file path is fetched from the environment variable `FIREBASE_KEY_PATH`. If the variable is not set, the default value `locateyourself.json` is used.

    Raises:
        ValueError: If the credentials file is not found or cannot be accessed.
    """

    FIREBASE_KEY_PATH = os.getenv("FIREBASE_KEY_PATH", "locateyourself.json")

    if not os.path.exists(FIREBASE_KEY_PATH):
        raise ValueError(f"Firebase credentials file '{FIREBASE_KEY_PATH}' not found.")


    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    initialize_app(cred, {
        "databaseURL": "https://locateyourself-6e64f-default-rtdb.firebaseio.com/"
    })

print("Firebase initialized.")
print(f"Using Firebase credentials file: {"locateyourself.json"}")
