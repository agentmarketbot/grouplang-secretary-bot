import os

class Config:
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
    MARKETROUTER_API_KEY = os.environ.get('MARKETROUTER_API_KEY')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME', 'conversations_db')
    DB_USER = os.environ.get('DB_USER', 'user')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
