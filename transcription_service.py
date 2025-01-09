from abc import ABC, abstractmethod

class TranscriptionService(ABC):
    @abstractmethod
    def transcribe_audio(self, file_url: str) -> str:
        pass
