import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = True
    GOOGLE_APPLICATION_CREDENTIALS = "./service-credentials.json"
    GOOGLE_ACOUNT_CREDENTIALS = "./service_account.json"
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    MODEL_ID = os.getenv("MODEL_ID")
    MODEL_PATH = os.getenv("MODEL_PATH")
    