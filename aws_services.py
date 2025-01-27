import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class AWSServices:
    def __init__(self, region_name='us-east-1'):
        self.region_name = region_name
        self.s3_client = boto3.client('s3', region_name=region_name)
        self.transcribe_client = boto3.client('transcribe', region_name=region_name)
        self.TEMP_BUCKET = 'audio-transcribe-temp'

    def setup_bucket_lifecycle(self):
        """Configure lifecycle policy to delete objects after 24 hours"""
        try:
            lifecycle_config = {
                'Rules': [
                    {
                        'ID': 'DeleteAfter24Hours',
                        'Status': 'Enabled',
                        'Prefix': '',
                        'Expiration': {'Days': 1}
                    }
                ]
            }
            
            self.s3_client.put_bucket_lifecycle_configuration(
                Bucket=self.TEMP_BUCKET,
                LifecycleConfiguration=lifecycle_config
            )
            logger.info(f"Successfully configured lifecycle policy for bucket {self.TEMP_BUCKET}")
            
        except ClientError as e:
            logger.error(f"Failed to set lifecycle policy: {str(e)}")
            raise

    def transcribe_audio(self, audio_file_path, job_name):
        """
        Upload audio file to S3 and transcribe it with proper error handling
        and cleanup
        """
        try:
            # Upload to S3
            s3_key = f"temp_audio/{job_name}"
            self.s3_client.upload_file(
                audio_file_path,
                self.TEMP_BUCKET,
                s3_key
            )
            logger.info(f"Successfully uploaded {audio_file_path} to S3")

            # Start transcription job
            job_uri = f"s3://{self.TEMP_BUCKET}/{s3_key}"
            self.transcribe_client.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': job_uri},
                MediaFormat='mp3',  # Adjust based on input format
                LanguageCode='en-US'  # Adjust based on requirements
            )

            # Wait for completion
            while True:
                status = self.transcribe_client.get_transcription_job(
                    TranscriptionJobName=job_name
                )
                job_status = status['TranscriptionJob']['TranscriptionJobStatus']
                
                if job_status in ['COMPLETED', 'FAILED']:
                    break

            # Cleanup temp file regardless of transcription success
            try:
                self.s3_client.delete_object(
                    Bucket=self.TEMP_BUCKET,
                    Key=s3_key
                )
                logger.info(f"Cleaned up temporary file {s3_key}")
            except ClientError as e:
                logger.warning(f"Failed to delete temporary file {s3_key}: {str(e)}")
                # Don't raise here as the file will be cleaned by lifecycle policy

            if job_status == 'COMPLETED':
                return status['TranscriptionJob']['Transcript']['TranscriptFileUri']
            else:
                error_message = status['TranscriptionJob'].get('FailureReason', 'Unknown error')
                raise Exception(f"Transcription failed: {error_message}")

        except ClientError as e:
            logger.error(f"AWS operation failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Transcription process failed: {str(e)}")
            raise