# GroupLang-secretary-bot

GroupLang-secretary-bot is a Telegram bot that transcribes voice messages, summarizes the content, and allows users to tip for the service. It utilizes AWS services for transcription and a custom API for summarization. The bot is designed to be deployed as an AWS Lambda function.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Getting Started](#getting-started)
- [Deployment](#deployment)
- [API Reference](#api-reference)
- [Contributing](#contributing)

## Features

- Transcribes voice messages using either AWS Transcribe or OpenAI Whisper API
- Flexible transcription service selection through configuration
- Summarizes transcribed text using a custom API
- Allows users to tip for the service
- Secures handling of API keys and tokens
- Is deployable as an AWS Lambda function

## Prerequisites

- Poetry for dependency management
- Telegram Bot Token
- MarketRouter API Key
- One of the following transcription services:
  - AWS account with Transcribe access, or
  - OpenAI API key for Whisper API access

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

## Getting Started

To quickly get started with the GroupLang-secretary-bot, follow these steps:

1. Clone the repository and navigate into the project directory.
2. Install Poetry and the project dependencies.
3. Set up the necessary environment variables as described in the Configuration section.
4. Start the bot using the provided command.
5. Interact with the bot on Telegram by sending voice messages.

1. Set up environment variables:
   - `TELEGRAM_BOT_TOKEN`: Your Telegram Bot Token
   - `AWS_ACCESS_KEY_ID`: Your AWS Access Key ID
   - `AWS_SECRET_ACCESS_KEY`: Your AWS Secret Access Key
   - `MARKETROUTER_API_KEY`: Your MarketRouter API Key

2. Configures AWS credentials:
   - Either set up the AWS CLI or use environment variables as mentioned above

## Configuration

1. Set up environment variables:
   - `TELEGRAM_BOT_TOKEN`: Your Telegram Bot Token
   - `MARKETROUTER_API_KEY`: Your MarketRouter API Key
   - `TRANSCRIPTION_SERVICE`: Choose between 'aws' (default) or 'openai'

   For AWS Transcribe:
   - `AWS_ACCESS_KEY_ID`: Your AWS Access Key ID
   - `AWS_SECRET_ACCESS_KEY`: Your AWS Secret Access Key
   - `AWS_REGION`: AWS region (defaults to 'us-east-1')

   For OpenAI Whisper:
   - `OPENAI_API_KEY`: Your OpenAI API key (required if using OpenAI transcription)

2. Configure transcription service:
   - For AWS Transcribe:
     - Set up the AWS CLI with `aws configure` or use environment variables as mentioned above
     - Ensure your AWS IAM user has necessary permissions for AWS Transcribe
   - For OpenAI Whisper:
     - Obtain an API key from OpenAI
     - Set `TRANSCRIPTION_SERVICE=openai` and provide `OPENAI_API_KEY`

1. Activate the Poetry virtual environment:
   ```
   poetry shell
   ```

2. Start the bot:
   ```
   uvicorn main:app --reload
   ```

3. On Telegram, start a conversation with the bot or add it to a group

4. Sends a voice message to the bot

5. The bot transcribes the audio, summarizes the content, and sends the result back

6. Users can tip using the inline button provided in the response

## Usage

1. Activate the Poetry virtual environment:
   ```
   poetry shell
   ```

2. Start the bot:
   ```
   uvicorn main:app --reload
   ```

3. In Telegram, start a conversation with the bot or add it to a group.

4. Send a voice message to the bot.

5. The bot will transcribe the audio, summarize the content, and send the result back.

6. Users can tip using the inline button provided with the response.

## Contributing

We welcome contributions to the GroupLang-secretary-bot! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request. Please ensure that your contributions align with the project's coding standards and include appropriate tests.

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
  - OpenAI Whisper API: For audio transcription using OpenAI's state-of-the-art model
- MarketRouter API: For text summarization and reward submission

Refer to the respective documentation for more details:
- [AWS Transcribe Documentation](https://docs.aws.amazon.com/transcribe/)
- [OpenAI Whisper API Documentation](https://platform.openai.com/docs/guides/speech-to-text)
- MarketRouter API Documentation (contact provider)
