import os
from app import create_app
from dotenv import load_dotenv


load_dotenv()
DEBUG = os.getenv("DEBUG") == "True"

app = create_app()

if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)