# GroupLang-secretary-bot

GroupLang-secretary-bot is a Telegram bot that transcribes voice messages, summarizes the content, and allows users to tip for the service. It uses AWS services for transcription and a custom API for summarization. The bot is designed to be deployed as an AWS Lambda function.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Deployment](#deployment)
- [API Reference](#api-reference)

## Features

- Flexible voice message transcription using either:
  - AWS Transcribe
  - OpenAI Whisper API
- Summarize transcribed text using a custom API
- Allow users to tip for the service
- Secure handling of API keys and tokens
- Configurable transcription service selection
- Deployable as an AWS Lambda function

## Prerequisites

- Poetry for dependency management
- One of the following transcription service accounts:
  - AWS account with Transcribe access
  - OpenAI API account with Whisper API access
- Telegram Bot Token
- MarketRouter API Key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/GroupLang-secretary-bot.git
   cd GroupLang-secretary-bot
   ```

2. Install Poetry if you haven't already:
   ```
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Install dependencies using Poetry:
   ```
   poetry install
   ```

## Configuration

1. Set up environment variables:
   
   Required for all configurations:
   - `TELEGRAM_BOT_TOKEN`: Your Telegram Bot Token
   - `MARKETROUTER_API_KEY`: Your MarketRouter API Key
   - `TRANSCRIPTION_SERVICE`: Choose between 'aws' or 'openai' (defaults to 'aws' if not set)

   Required for AWS Transcribe:
   - `AWS_ACCESS_KEY_ID`: Your AWS Access Key ID
   - `AWS_SECRET_ACCESS_KEY`: Your AWS Secret Access Key
   - `AWS_REGION`: AWS region (defaults to 'us-east-1' if not set)

   Required for OpenAI Whisper:
   - `OPENAI_API_KEY`: Your OpenAI API Key

2. Configure credentials based on your chosen transcription service:
   - For AWS: Either set up the AWS CLI or use AWS environment variables as mentioned above
   - For OpenAI: Ensure you have a valid API key with access to the Whisper API

## Usage

1. Activate the Poetry virtual environment:
   ```
   poetry shell
   ```

2. Start the bot:
   ```
   uvicorn main:app --reload
   ```

3. In Telegram, start a conversation with the bot or add it to a group

4. Send a voice message to the bot

5. The bot will transcribe the audio, summarize the content, and send the result back

6. Users can tip using the inline button provided with the response

## Adding or Updating Dependencies

To add a new package:
```
poetry add package_name
```

To update all packages:
```
poetry update
```

To update a specific package:
```
poetry update package_name
```

## API Reference

The bot uses the following external APIs:

- Transcription Services (configurable):
  - AWS Transcribe: For audio transcription using AWS services
  - OpenAI Whisper API: For audio transcription using OpenAI's model
- MarketRouter API: For text summarization and reward submission

For more information, refer to:
- [AWS Transcribe Documentation](https://docs.aws.amazon.com/transcribe/)
- [OpenAI Whisper API Documentation](https://platform.openai.com/docs/guides/speech-to-text)
- MarketRouter API Documentation (refer to your API provider)