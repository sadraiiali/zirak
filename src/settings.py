from pydantic import BaseModel, SecretStr
from typing import List, Optional
import os
from pathlib import Path
from pydantic_yaml import parse_yaml_raw_as
import dotenv

# Define base directory
BASE_DIR = Path(__file__).parent.parent

# Load environment variables from .env file
dotenv.load_dotenv(os.path.join(BASE_DIR, ".env"))


class MastodonCredentials(BaseModel):
    """Secure settings loaded from environment variables"""
    client_id: SecretStr
    client_secret: SecretStr
    access_token: SecretStr


class MastodonConfig(BaseModel):
    """YAML-based configuration for Mastodon settings"""
    instance_url: str
    alt_instances: List[str]
    app_name: str
    session_file: str
    notification_limit: int = 15
    notification_interval: int = 60  # Seconds between notification checks


class LoggingConfig(BaseModel):
    """Logging configuration"""
    level: str = "INFO"
    to_file: bool = False
    log_dir: str = "logs"


class AppConfig(BaseModel):
    """Root configuration model that includes all sub-configurations"""
    mastodon: MastodonConfig
    logging: Optional[LoggingConfig] = LoggingConfig()


class Settings:
    """Main settings container"""
    def __init__(self):
        # Load YAML config
        yaml_path = os.path.join(BASE_DIR, "env.yml")
        with open(yaml_path, 'r') as f:
            yaml_content = f.read()
        
        # Parse YAML using pydantic-yaml
        app_config = parse_yaml_raw_as(AppConfig, yaml_content)
        self.mastodon = app_config.mastodon
        self.logging = app_config.logging
        
        # Load credentials from environment variables
        self.credentials = MastodonCredentials(
            client_id=SecretStr(os.environ.get("MASTODON_CLIENT_ID", "")),
            client_secret=SecretStr(os.environ.get("MASTODON_CLIENT_SECRET", "")),
            access_token=SecretStr(os.environ.get("MASTODON_ACCESS_TOKEN", ""))
        )
        
        # Debug output to verify environment variables are loaded
        print(f"Loaded credentials for client ID: {self.credentials.client_id.get_secret_value()[:8]}...")
    
    def get_absolute_path(self, relative_path):
        """Convert a relative path to absolute path based on project root"""
        return os.path.join(BASE_DIR, relative_path)


# Create a singleton settings instance
settings = Settings()
