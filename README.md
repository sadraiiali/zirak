# Zirak AI - Mastodon Bot

Zirak AI is a Mastodon bot designed to interact with users, respond to mentions, and perform automated tasks using Large Language Models (LLMs). It leverages the Mastodon API and Google's Vertex AI to provide intelligent and engaging interactions on the decentralized social network.

## Features

-   **Intelligent Responses:** Uses Vertex AI to generate context-aware responses to mentions.
-   **Notification Handling:** Monitors and processes various Mastodon notifications (mentions, follows, favorites, reblogs).
-   **Thread Tracking:**  Fetches and analyzes entire conversation threads to provide better context for AI responses.
-   **Configurable:**  Settings managed via YAML configuration files and environment variables.
-   **Asynchronous Polling:** Uses `asyncio` for efficient notification polling.
-   **Authentication Checker:** Includes a utility script to verify Mastodon API credentials.

## Project Structure

```
zirak/
├── .env.example              # Example environment variables
├── env.yml                   # YAML configuration file
├── main.py                   # Main application entry point
├── README.md                 # This file
├── src/                      # Source code directory
│   ├── commands/             # Command-line scripts
│   │   └── check_auth.py     # Script to check Mastodon authentication
│   ├── helpers/              # Helper functions and utilities
│   │   └── prompts.py        # Functions for loading prompts
│   ├── llms/                 # LLM interface implementations
│   │   ├── General.py        # Abstract base class for LLMs
│   │   └── VertexAI.py       # Vertex AI implementation
│   ├── mastodon/             # Mastodon API client
│   │   └── mastodon_client.py# Mastodon client wrapper
│   ├── notifications.py      # Notification handling logic
│   ├── prompts/              # Prompt files for LLM
│   │   ├── mastodon_system_prompt.txt
│   │   └── mastodon_user_prompt.txt
│   ├── logger.py             # Logging setup
│   └── settings.py           # Application settings and configuration
├── test.py                   # Testing script
└── env.yml                   # Environment configuration file
```

## Requirements

-   Python 3.8+
-   `mastodon.py`
-   `pydantic`
-   `pydantic-yaml`
-   `python-dotenv`
-   `google-cloud-aiplatform`
-   `google-auth`
-   `google-generativeai`
-   `html2text`
-   `uv`

Install the dependencies:

```bash
uv sync
```

## Setup

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd zirak
    ```

2.  **Create a `.env` file:**

    Copy the contents of `.env.example` to a new file named `.env` and fill in your Mastodon API credentials.

    ```bash
    cp .env.example .env
    nano .env
    ```

    ```
    MASTODON_CLIENT_ID=your_client_id_here
    MASTODON_CLIENT_SECRET=your_client_secret_here
    MASTODON_ACCESS_TOKEN=your_access_token_here
    ```

3.  **Configure `env.yml`:**

    Adjust the settings in `env.yml` to match your desired configuration.  Pay attention to the `instance_url` and other Mastodon-related settings.

4.  **Set up Google Cloud Credentials:**

    *   Create a Google Cloud project and enable the Vertex AI API.
    *   Create a service account with the necessary permissions.
    *   Download the service account key as a JSON file and place it in the `data/` directory (you might need to create this directory).  The path to this file should be specified in `src/notifications.py`.

## Usage

1.  **Run the bot:**

    ```bash
    uv run python main.py
    ```

2.  **Check Authentication:**

    You can use the `check_auth.py` script to verify your Mastodon credentials:

    ```bash
    uv run python src/commands/check_auth.py
    ```

## Configuration

The bot's behavior is configured using a combination of environment variables (for sensitive information) and a YAML configuration file (`env.yml`).

### Environment Variables

-   `MASTODON_CLIENT_ID`: The client ID of your Mastodon application.
-   `MASTODON_CLIENT_SECRET`: The client secret of your Mastodon application.
-   `MASTODON_ACCESS_TOKEN`: The access token for your Mastodon account.

### `env.yml`

```yaml
# Mastodon API Configuration
mastodon:
  instance_url: "https://khiar.net"
  alt_instances: []
  app_name: "zirak_ai"
  session_file: "mastodon_session.pickle"
  notification_limit: 15
  notification_interval: 1  # Seconds between notification polling

# Logging Configuration
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
  to_file: false
  log_dir: "logs"
```

## License

This project is licensed under the GPL-3.0-or-later License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to discuss potential improvements.
