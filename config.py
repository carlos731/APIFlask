from dotenv import load_dotenv
import os

# Carregar as variáveis do arquivo .env
load_dotenv()

DEBUG = True

USERNAME = os.getenv('DB_USERNAME', 'default_user')
PASSWORD = os.getenv('DB_PASSWORD', 'default_password')
SERVER = os.getenv('DB_SERVER', 'localhost')
DB = os.getenv('DB_NAME', 'default_db')

SQLALCHEMY_DATABASE_URI = f'mysql://{USERNAME}:{PASSWORD}@{SERVER}/{DB}'
SQLALCHEMY_TRACK_MODIFICATIONS = True
