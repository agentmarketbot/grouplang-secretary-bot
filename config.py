import os

class Config:
    # Telegram Configuration
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    # AWS Configuration
    AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    
    # MarketRouter Configuration
    MARKETROUTER_API_KEY = os.environ.get('MARKETROUTER_API_KEY')
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # Transcription Service Configuration
    # Options: 'aws' or 'openai'
    TRANSCRIPTION_SERVICE = os.environ.get('TRANSCRIPTION_SERVICE', 'aws')
    
    @classmethod
    def get_transcription_config(cls):
        """Get the configuration for the selected transcription service."""
        if cls.TRANSCRIPTION_SERVICE == 'aws':
            if not all([cls.AWS_ACCESS_KEY_ID, cls.AWS_SECRET_ACCESS_KEY]):
                raise ValueError("AWS credentials are required for AWS transcription service")
        elif cls.TRANSCRIPTION_SERVICE == 'openai':
            if not cls.OPENAI_API_KEY:
                raise ValueError("OpenAI API key is required for OpenAI transcription service")
        else:
            raise ValueError(f"Unknown transcription service: {cls.TRANSCRIPTION_SERVICE}")
