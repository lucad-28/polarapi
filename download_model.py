from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_ACOUNT_CREDENTIALS = "./service_account.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]
MODEL_ID = os.getenv("MODEL_ID")
MODEL_PATH = os.getenv("MODEL_PATH")

gauth = GoogleAuth()
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_ACOUNT_CREDENTIALS, SCOPES)

drive = GoogleDrive(gauth)

model = None
model_path = MODEL_PATH


print("Descargando modelo...", MODEL_ID)
file = drive.CreateFile({'id': MODEL_ID})
file.GetContentFile(model_path)