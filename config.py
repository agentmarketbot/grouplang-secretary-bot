import os

class Config:
    # Telegram Configuration
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    # AWS Configuration
    AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # MarketRouter Configuration
    MARKETROUTER_API_KEY = os.environ.get('MARKETROUTER_API_KEY')
    
    # Transcription Service Configuration
    TRANSCRIPTION_SERVICE = os.environ.get('TRANSCRIPTION_SERVICE', 'aws')  # 'aws' or 'openai'
