"""
AWS Services Module for Audio Transcription
-----------------------------------------

This module handles AWS S3 and Transcribe services integration with automatic cleanup
of temporary audio files. It implements a 24-hour lifecycle policy for the S3 bucket
to ensure temporary files are automatically removed, addressing potential storage costs
and security concerns.

Features:
- Automatic cleanup of temporary audio files after 24 hours via S3 lifecycle policy
- Immediate cleanup after successful or failed transcription
- Comprehensive error handling and logging
- Verification methods for lifecycle policy configuration

Usage:
    aws = AWSServices()
    aws.initialize_service()  # Sets up bucket and lifecycle policy
    aws.verify_lifecycle_policy()  # Verifies the lifecycle policy is active
    transcript_uri = aws.transcribe_audio('path/to/audio.mp3')

Fixes #158: Implements S3 Lifecycle Policy for Temporary Audio Cleanup
"""

import boto3
import logging
import time
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class AWSServices:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.transcribe_client = boto3.client('transcribe')
        self.TEMP_BUCKET = 'audio-transcribe-temp'

    def setup_bucket_lifecycle(self):
        """
        Sets up lifecycle policy to automatically delete objects after 24 hours.
        """
        try:
            lifecycle_config = {
                'Rules': [
                    {
                        'ID': 'DeleteTempAudioAfter24Hours',
                        'Status': 'Enabled',
                        'Expiration': {'Days': 1},
                        'Filter': {'Prefix': ''}  # Apply to all objects
                    }
                ]
            }
            
            self.s3_client.put_bucket_lifecycle_configuration(
                Bucket=self.TEMP_BUCKET,
                LifecycleConfiguration=lifecycle_config
            )
            logger.info(f"Successfully set lifecycle policy on bucket {self.TEMP_BUCKET}")
            return True
        except ClientError as e:
            logger.error(f"Failed to set lifecycle policy: {str(e)}")
            return False

    def transcribe_audio(self, audio_file_path, language_code='en-US'):
        """
        Transcribes audio file using AWS Transcribe service with proper cleanup.
        """
        try:
            # Upload file to S3
            file_name = audio_file_path.split('/')[-1]
            s3_path = f"temp/{file_name}"
            
            self.s3_client.upload_file(
                audio_file_path,
                self.TEMP_BUCKET,
                s3_path
            )
            logger.info(f"Successfully uploaded {file_name} to S3")

            # Start transcription job
            job_name = f"transcribe_{file_name}_{int(time.time())}"
            self.transcribe_client.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': f"s3://{self.TEMP_BUCKET}/{s3_path}"},
                MediaFormat=file_name.split('.')[-1],
                LanguageCode=language_code
            )

            # Wait for completion
            while True:
                status = self.transcribe_client.get_transcription_job(
                    TranscriptionJobName=job_name
                )
                if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                    break
                time.sleep(5)

            # Clean up the temporary file regardless of transcription success
            try:
                self.s3_client.delete_object(
                    Bucket=self.TEMP_BUCKET,
                    Key=s3_path
                )
                logger.info(f"Successfully deleted temporary file {s3_path}")
            except ClientError as e:
                logger.warning(f"Failed to delete temporary file {s3_path}: {str(e)}")
                # Don't raise this error as the file will be cleaned up by lifecycle policy

            if status['TranscriptionJob']['TranscriptionJobStatus'] == 'FAILED':
                raise Exception(f"Transcription job failed: {status['TranscriptionJob'].get('FailureReason', 'Unknown error')}")

            return status['TranscriptionJob']['Transcript']['TranscriptFileUri']

        except Exception as e:
            logger.error(f"Error in transcribe_audio: {str(e)}")
            raise

    def initialize_service(self):
        """
        Initializes the AWS services and ensures proper configuration.
        """
        try:
            # Ensure bucket exists
            self.s3_client.head_bucket(Bucket=self.TEMP_BUCKET)
            # Setup lifecycle policy
            self.setup_bucket_lifecycle()
            return True
        except ClientError as e:
            logger.error(f"Failed to initialize AWS services: {str(e)}")
            return False

    def verify_lifecycle_policy(self):
        """
        Verifies that the lifecycle policy is correctly configured.
        Returns the current lifecycle rules if they exist.
        """
        try:
            response = self.s3_client.get_bucket_lifecycle_configuration(
                Bucket=self.TEMP_BUCKET
            )
            rules = response.get('Rules', [])
            for rule in rules:
                if rule.get('ID') == 'DeleteTempAudioAfter24Hours':
                    logger.info("Lifecycle policy verified: 24-hour deletion rule is active")
                    return True
            logger.warning("24-hour deletion rule not found in lifecycle policies")
            return False
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
                logger.error("No lifecycle configuration found on bucket")
            else:
                logger.error(f"Error verifying lifecycle policy: {str(e)}")
            return False