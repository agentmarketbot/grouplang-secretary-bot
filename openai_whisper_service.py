import requests
from transcription_service import TranscriptionService

class OpenAIWhisperService(TranscriptionService):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = 'https://api.openai.com/v1/whisper'

    def transcribe_audio(self, file_url: str) -> str:
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'file_url': file_url
        }
        response = requests.post(f'{self.base_url}/transcriptions', headers=headers, json=data)
        response.raise_for_status()
        return response.json()['transcription']
