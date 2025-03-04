import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from google.cloud.firestore_v1.base_query import FieldFilter
import pandas as pd
from app import app as flask_app
from datetime import datetime, timedelta

GOOGLE_APPLICATION_CREDENTIALS = flask_app.config['GOOGLE_APPLICATION_CREDENTIALS']
cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
app = firebase_admin.initialize_app(cred)
db = firestore.client()

def fetch_history_data():
    history_ref = db.collection('history')
    history_data = history_ref.stream()
    history_data = [doc.to_dict() for doc in history_data]
    return pd.DataFrame(history_data)

def fetch_history_data_by_devicesIds(deviceIds):
    history_ref = db.collection('history')
    history_data = (
        history_ref
        .where(filter=FieldFilter("deviceId", "in", deviceIds))  # Filtrar por deviceIds
        .stream()  # Obtener los documentos como flujo de datos
    )   
    history_data = [doc.to_dict() for doc in history_data]
    return pd.DataFrame(history_data)

def fetch_history_by_devicesIds(deviceIds, final_day= datetime.now()):
    history_ref = db.collection('history')
    last_day = final_day - timedelta(hours=5)
    history_data = (
        history_ref
        .where(filter=FieldFilter("deviceId", "in", deviceIds))  # Filtrar por deviceIds
        .where(filter=FieldFilter("timestamp", ">=", last_day))  # Filtrar por tiempo
        .order_by("timestamp", direction=firestore.Query.DESCENDING)
        .stream()  # Obtener los documentos como flujo de datos
    )   
    history_data = [doc.to_dict() for doc in history_data]
    return pd.DataFrame(history_data)

def update_history_data(deviceId, record):
    history_ref = db.collection('history')
    history_ref.add({
        "deviceId": deviceId,
        "timestamp": record['timestamp'],
        "temperature": record['temperature'],
        "volume": record['volume'],
        "cooling": record['cooling']
    })