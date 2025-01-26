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

- Supports multiple transcription services:
  - AWS Transcribe (default)
  - OpenAI Whisper API
- Summarizes transcribed text using a custom API
- Allows users to tip for the service
- Secures handling of API keys and tokens
- Is deployable as an AWS Lambda function

## Prerequisites

- Poetry for dependency management
- Telegram Bot Token
- MarketRouter API Key
- One of the following transcription service configurations:
  - AWS account with Transcribe access (default)
  - OpenAI API key for Whisper API

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

1. Set up common environment variables:
   - `TELEGRAM_BOT_TOKEN`: Your Telegram Bot Token
   - `MARKETROUTER_API_KEY`: Your MarketRouter API Key

2. Select and configure your transcription service using `TRANSCRIPTION_SERVICE`:
   - For AWS Transcribe (default, `TRANSCRIPTION_SERVICE=aws`):
     - `AWS_ACCESS_KEY_ID`: Your AWS Access Key ID
     - `AWS_SECRET_ACCESS_KEY`: Your AWS Secret Access Key
     - `AWS_REGION`: AWS region (default: 'us-east-1')
     - Ensure your AWS IAM user has the necessary permissions for AWS Transcribe
   
   - For OpenAI Whisper (`TRANSCRIPTION_SERVICE=openai`):
     - `OPENAI_API_KEY`: Your OpenAI API key

Example configuration for AWS Transcribe:
```bash
export TRANSCRIPTION_SERVICE=aws
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=us-east-1
```

Example configuration for OpenAI Whisper:
```bash
export TRANSCRIPTION_SERVICE=openai
export OPENAI_API_KEY=your_openai_api_key
```

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

### Transcription Services
- AWS Transcribe (default)
  - Used when `TRANSCRIPTION_SERVICE=aws`
  - Requires AWS credentials and appropriate IAM permissions
  - [AWS Transcribe Documentation](https://docs.aws.amazon.com/transcribe/)

- OpenAI Whisper API
  - Used when `TRANSCRIPTION_SERVICE=openai`
  - Requires OpenAI API key
  - [OpenAI Whisper API Documentation](https://platform.openai.com/docs/api-reference/audio)

### Summarization Service
- MarketRouter API
  - Used for text summarization and reward submission
  - Requires MarketRouter API key

Refer to the respective documentation for more details on these APIs.
