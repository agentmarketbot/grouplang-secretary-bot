import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class AWSServices:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.transcribe_client = boto3.client('transcribe')
        self.bucket_name = 'audio-transcribe-temp'

    def setup_bucket_lifecycle(self):
        """
        Sets up lifecycle policy to automatically delete objects after 24 hours.
        Fixes #156
        """
        try:
            lifecycle_config = {
                'Rules': [
                    {
                        'ID': 'Delete temporary audio files',
                        'Status': 'Enabled',
                        'Prefix': '',  # Apply to all objects
                        'Expiration': {'Days': 1},  # Delete after 24 hours
                    }
                ]
            }
            
            self.s3_client.put_bucket_lifecycle_configuration(
                Bucket=self.bucket_name,
                LifecycleConfiguration=lifecycle_config
            )
            logger.info(f"Successfully set lifecycle policy on bucket {self.bucket_name}")
            return True
        except ClientError as e:
            logger.error(f"Failed to set lifecycle policy: {str(e)}")
            return False

    def upload_audio_for_transcription(self, file_path, object_key):
        """
        Uploads an audio file to S3 for transcription.
        """
        try:
            self.s3_client.upload_file(file_path, self.bucket_name, object_key)
            logger.info(f"Successfully uploaded {object_key} to {self.bucket_name}")
            return True
        except ClientError as e:
            logger.error(f"Failed to upload file: {str(e)}")
            return False

    def transcribe_audio(self, object_key, language_code='en-US'):
        """
        Transcribes an audio file using Amazon Transcribe.
        The file will be automatically deleted after 24 hours by the lifecycle policy.
        """
        try:
            job_name = f"transcription_{object_key.replace('/', '_')}"
            job_uri = f"s3://{self.bucket_name}/{object_key}"
            
            self.transcribe_client.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': job_uri},
                MediaFormat=object_key.split('.')[-1].lower(),
                LanguageCode=language_code
            )
            
            logger.info(f"Started transcription job: {job_name}")
            return job_name
        except ClientError as e:
            logger.error(f"Failed to start transcription: {str(e)}")
            # Even if transcription fails, the lifecycle policy will clean up the file
            return None

    def cleanup_transcription(self, object_key):
        """
        Explicitly delete an audio file after successful transcription.
        This is optional since the lifecycle policy will handle cleanup,
        but useful for immediate cleanup after successful processing.
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            logger.info(f"Successfully deleted {object_key} from {self.bucket_name}")
            return True
        except ClientError as e:
            logger.error(f"Failed to delete file: {str(e)}")
            return False