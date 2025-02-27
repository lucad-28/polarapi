import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import pandas as pd
from app import app as flask_app

GOOGLE_APPLICATION_CREDENTIALS = flask_app.config['GOOGLE_APPLICATION_CREDENTIALS']
cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
app = firebase_admin.initialize_app(cred)
db = firestore.client()

def fetch_history_data():
    history_ref = db.collection('history')
    history_data = history_ref.stream()
    history_data = [doc.to_dict() for doc in history_data]
    return pd.DataFrame(history_data)