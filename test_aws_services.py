import unittest
from unittest.mock import MagicMock, patch
from aws_services import AWSServices

class TestAWSServices(unittest.TestCase):
    def setUp(self):
        # Mock both S3 and Transcribe clients
        self.mock_s3_client = MagicMock()
        self.mock_transcribe_client = MagicMock()
        
        with patch('boto3.client') as mock_boto3_client:
            mock_boto3_client.side_effect = [self.mock_s3_client, self.mock_transcribe_client]
            self.aws_services = AWSServices(region_name='us-east-1')
            # Replace the clients with our mocks
            self.aws_services.s3_client = self.mock_s3_client
            self.aws_services.transcribe_client = self.mock_transcribe_client

    def test_setup_bucket_lifecycle(self):
        # Test lifecycle configuration
        self.aws_services.setup_bucket_lifecycle()
        
        # Verify the lifecycle configuration was called with correct parameters
        self.mock_s3_client.put_bucket_lifecycle_configuration.assert_called_once()
        call_args = self.mock_s3_client.put_bucket_lifecycle_configuration.call_args[1]
        
        self.assertEqual(call_args['Bucket'], 'audio-transcribe-temp')
        self.assertEqual(call_args['LifecycleConfiguration']['Rules'][0]['Expiration']['Days'], 1)
        self.assertEqual(call_args['LifecycleConfiguration']['Rules'][0]['Status'], 'Enabled')

    @patch('os.path.getsize')
    def test_transcribe_audio_success(self, mock_getsize):
        # Mock file size for upload
        mock_getsize.return_value = 1024
        
        # Mock successful transcription
        self.mock_transcribe_client.get_transcription_job.return_value = {
            'TranscriptionJob': {
                'TranscriptionJobStatus': 'COMPLETED',
                'Transcript': {
                    'TranscriptFileUri': 'https://example.com/transcript.json'
                }
            }
        }
        
        # Test transcription
        result = self.aws_services.transcribe_audio('test.mp3', 'test-job')
        
        # Verify S3 operations
        self.mock_s3_client.upload_file.assert_called_once()
        self.mock_s3_client.delete_object.assert_called_once()
        
        # Verify transcribe operations
        self.mock_transcribe_client.start_transcription_job.assert_called_once()
        self.assertEqual(result, 'https://example.com/transcript.json')

    @patch('os.path.getsize')
    def test_transcribe_audio_failure(self, mock_getsize):
        # Mock file size for upload
        mock_getsize.return_value = 1024
        
        # Mock failed transcription
        self.mock_transcribe_client.get_transcription_job.return_value = {
            'TranscriptionJob': {
                'TranscriptionJobStatus': 'FAILED',
                'FailureReason': 'Test failure'
            }
        }
        
        # Test transcription failure
        with self.assertRaises(Exception) as context:
            self.aws_services.transcribe_audio('test.mp3', 'test-job')
        
        # Verify cleanup was still attempted
        self.mock_s3_client.delete_object.assert_called_once()
        self.assertTrue('Test failure' in str(context.exception))

if __name__ == '__main__':
    unittest.main()