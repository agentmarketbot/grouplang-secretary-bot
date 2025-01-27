import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class S3BucketManager:
    def __init__(self, bucket_name='audio-transcribe-temp'):
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name
        
    def setup_bucket_lifecycle(self):
        """
        Sets up a lifecycle policy to delete objects after 24 hours
        """
        try:
            lifecycle_config = {
                'Rules': [
                    {
                        'ID': 'Delete after 24 hours',
                        'Status': 'Enabled',
                        'Prefix': '',
                        'Expiration': {'Days': 1}
                    }
                ]
            }
            
            self.s3_client.put_bucket_lifecycle_configuration(
                Bucket=self.bucket_name,
                LifecycleConfiguration=lifecycle_config
            )
            logger.info(f"Successfully set lifecycle policy for bucket {self.bucket_name}")
            return True
            
        except ClientError as e:
            logger.error(f"Failed to set lifecycle policy: {str(e)}")
            return False

    def upload_audio(self, file_path, s3_key):
        """
        Uploads an audio file to S3
        """
        try:
            self.s3_client.upload_file(file_path, self.bucket_name, s3_key)
            logger.info(f"Successfully uploaded {file_path} to {self.bucket_name}/{s3_key}")
            return True
        except ClientError as e:
            logger.error(f"Failed to upload file: {str(e)}")
            return False

    def delete_audio(self, s3_key):
        """
        Deletes an audio file from S3
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            logger.info(f"Successfully deleted {s3_key} from {self.bucket_name}")
            return True
        except ClientError as e:
            logger.error(f"Failed to delete file: {str(e)}")
            return False

def transcribe_audio(audio_file_path, job_name):
    """
    Transcribes an audio file using AWS Transcribe
    """
    s3_manager = S3BucketManager()
    transcribe_client = boto3.client('transcribe')
    
    try:
        # Ensure bucket has lifecycle policy
        s3_manager.setup_bucket_lifecycle()
        
        # Upload audio file
        s3_key = f"temp/{job_name}.mp3"
        if not s3_manager.upload_audio(audio_file_path, s3_key):
            raise Exception("Failed to upload audio file")

        # Start transcription job
        s3_uri = f"s3://{s3_manager.bucket_name}/{s3_key}"
        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': s3_uri},
            MediaFormat='mp3',
            LanguageCode='en-US'
        )

        # Wait for completion
        while True:
            status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break

        # Clean up the temporary file regardless of transcription success
        s3_manager.delete_audio(s3_key)

        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            return status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        else:
            raise Exception(f"Transcription failed: {status['TranscriptionJob'].get('FailureReason', 'Unknown error')}")

    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        # Attempt to clean up even if transcription fails
        s3_manager.delete_audio(s3_key)
        raise