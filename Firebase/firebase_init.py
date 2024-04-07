
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

def init_firebase():

    if not firebase_admin._apps:
        cred = credentials.Certificate("Firebase/discordbot-34f67-firebase-adminsdk-yl0ef-fcdeaa0825.json")
        firebase_admin.initialize_app(cred)

    return firestore.client()
