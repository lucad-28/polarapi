import joblib
import os
from app import app as flask_app
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

import numpy as np
import pandas as pd

gauth = GoogleAuth()
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(flask_app.config["GOOGLE_ACOUNT_CREDENTIALS"], flask_app.config["SCOPES"])

drive = GoogleDrive(gauth)

model = None

def download_model():
    print("Descargando modelo...", flask_app.config["MODEL_ID"])
    file = drive.CreateFile({'id': flask_app.config["MODEL_ID"]})
    file.GetContentFile("modelo.pkl")


def load_model():
    global model
    if not os.path.exists("modelo.pkl"):
        download_model()

    model = joblib.load("modelo.pkl")
    print("Modelo cargado exitosamente.")

load_model()

def gen_random_data():
    # Configuración inicial
    np.random.seed(42)
    num_samples = 17280 * 2 # Número total de muestras
    interval = 5  # Intervalo de tiempo en segundos
    timestamps = pd.date_range(start="2025-2-28 08:10:01", periods=num_samples, freq=f"{interval}s")

    coolings = []
    temperatures = []
    volumes = []
    temp = 25  # Temperatura inicial
    volume = 1.012  # Volumen inicial del jarro en litros (suponiendo un jarro de 2L)
    evaporation_rate = 0.0005  # Pérdida de volumen por evaporación por cada paso de tiempo

    duration_cooling = np.random.uniform(0, 50)
    duration_heating = np.random.uniform(0, 100)
    i = 0
    temp_max = 24
    temp_min = 27
    while i < num_samples:

        if timestamps[i].hour < 9 or timestamps[i].hour > 21:
            temp_min = 23
            temp_max = 25
        elif 9 <= timestamps[i].hour < 13:
            temp_min = 24
            temp_max = 25.5
        else:
            temp_min = 23.5
            temp_max = 25.2
        

        temp_max += np.random.uniform(-1, 1) if timestamps[i].hour < 9 or timestamps[i].hour > 15 else np.random.uniform(-1, 1.5)
        temp_min += np.random.uniform(-1, 1) if timestamps[i].hour < 9 or timestamps[i].hour > 15 else np.random.uniform(-1, 1.5)

        if temp >= 25:  
            start_cooling = i
            while i - start_cooling < duration_cooling and temp >= temp_min + np.random.uniform(-1, 1) and i < num_samples:
                temp = temp - np.random.uniform(0.002, 0.01) if timestamps[i].hour < 18 and timestamps[i].hour > 9 else temp - np.random.uniform(0.001, 0.005)
                temperatures.append(temp)
                coolings.append(1)
                volume = volume - evaporation_rate if np.random.uniform(-1, 1) > 0  else volume + evaporation_rate
                volumes.append(volume)
                i += 1
        else:
            start_heating = i
            while i - start_heating < duration_heating and temp <= temp_max + np.random.uniform(-1, 1) and i < num_samples:
                temp = temp + np.random.uniform(0.002, 0.004) if timestamps[i].hour < 9 and timestamps[i].hour > 22 else temp + np.random.uniform(0.001, 0.005)
                temperatures.append(temp)
                coolings.append(0)
                volume = volume - evaporation_rate if np.random.uniform(-1, 1) > 0  else volume + evaporation_rate
                volumes.append(volume)
                i += 1

        duration_cooling = np.random.uniform(i, i + 75 if 9 <= timestamps[i-1].hour < 18 else i + 25 ) 
        duration_heating = np.random.uniform(i, i + 25 if 9 <= timestamps[i-1].hour < 18 else i + 75)  

    df = pd.DataFrame({"timestamp": timestamps, "temperature": temperatures, "cooling": coolings, "volume": volumes})
    df.index = pd.to_datetime(df.index)

    return df
