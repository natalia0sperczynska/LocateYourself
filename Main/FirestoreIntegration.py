import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firestore():
    cred = credentials.Certificate("C:/Users/tomek/PyCharmProjects/LocateYourself/Config/projekt1-8a8e0-firebase-adminsdk-i5gv9-6e7f912911.json")
    firebase_admin.initialize_app(cred)
    return firestore.client()

def write_user_to_firestore(db, user_data):
    db.collection("Users").add(user_data)
    print("User data uploaded to Firestore.")
