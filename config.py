import os

class Config:
    # Telegram Configuration
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    # Transcription Service Configuration
    TRANSCRIPTION_SERVICE = os.environ.get('TRANSCRIPTION_SERVICE', 'aws')  # 'aws' or 'openai'
    
    # AWS Configuration (required if TRANSCRIPTION_SERVICE='aws')
    AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    
    # OpenAI Configuration (required if TRANSCRIPTION_SERVICE='openai')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # MarketRouter Configuration
    MARKETROUTER_API_KEY = os.environ.get('MARKETROUTER_API_KEY')
    
    @classmethod
    def validate_config(cls):
        """Validate the configuration based on the selected transcription service."""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
            
        if not cls.MARKETROUTER_API_KEY:
            raise ValueError("MARKETROUTER_API_KEY environment variable is required")
            
        if cls.TRANSCRIPTION_SERVICE.lower() == 'aws':
            if not (cls.AWS_ACCESS_KEY_ID and cls.AWS_SECRET_ACCESS_KEY):
                raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are required for AWS transcription")
        elif cls.TRANSCRIPTION_SERVICE.lower() == 'openai':
            if not cls.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY environment variable is required for OpenAI transcription")
        else:
            raise ValueError("TRANSCRIPTION_SERVICE must be either 'aws' or 'openai'")
