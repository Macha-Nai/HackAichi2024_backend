import os
from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.environ.get('APP_ENV')

DB_USER = os.environ.get('MYSQL_USER')
DB_PASSWORD = os.environ.get('MYSQL_PASSWORD')
DB_HOST = os.environ.get('MYSQL_HOST')
DB_NAME = os.environ.get('MYSQL_DATABASE')

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET =  os.environ.get('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
TOKEN_URL = os.environ.get('TOKEN_URL')
AUTHORIZATION_BASE_URL = os.environ.get('AUTHORIZATION_BASE_URL')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')