import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import pandas as pd

cred = credentials.Certificate('service-credentials.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

def fetch_history_data():
    history_ref = db.collection('history')
    history_data = history_ref.stream()
    history_data = [doc.to_dict() for doc in history_data]
    return pd.DataFrame(history_data)