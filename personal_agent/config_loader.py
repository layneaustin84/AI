"""
Configuration Loader for Personal Agent
Handles tone profiles, API keys, and environment configuration
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Loads and manages configuration for the personal agent."""

    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize configuration loader.

        Args:
            config_dir: Path to config directory (defaults to ./config)
        """
        self.config_dir = Path(config_dir) if config_dir else Path(__file__).parent / "config"
        self.tone_profiles: Dict[str, Any] = {}
        self.defaults: Dict[str, Any] = {}
        self._load_env()
        self._load_tone_profiles()

    def _load_env(self) -> None:
        """Load environment variables from .env file."""
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            load_dotenv(env_path)
        else:
            logger.warning(f".env file not found at {env_path}. Please copy .env.example to .env and configure.")

    def _load_tone_profiles(self) -> None:
        """Load tone profiles from JSON configuration."""
        tone_profiles_path = self.config_dir / "tone_profiles.json"

        if not tone_profiles_path.exists():
            logger.error(f"Tone profiles file not found at {tone_profiles_path}")
            raise FileNotFoundError(f"Configuration file missing: {tone_profiles_path}")

        try:
            with open(tone_profiles_path, 'r') as f:
                config = json.load(f)
                self.tone_profiles = config.get("profiles", {})
                self.defaults = config.get("defaults", {})
                logger.info(f"Loaded {len(self.tone_profiles)} tone profiles")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in tone profiles: {e}")
            raise ValueError(f"Invalid configuration file: {e}")

    def get_tone_profile(self, profile_name: str) -> Dict[str, Any]:
        """
        Get a specific tone profile by name.

        Args:
            profile_name: Name of the tone profile

        Returns:
            Tone profile dictionary

        Raises:
            ValueError: If profile not found
        """
        if profile_name not in self.tone_profiles:
            available = ", ".join(self.tone_profiles.keys())
            raise ValueError(
                f"Tone profile '{profile_name}' not found. Available profiles: {available}"
            )
        return self.tone_profiles[profile_name]

    def get_default_profile_for_type(self, doc_type: str) -> str:
        """
        Get default tone profile for a document type.

        Args:
            doc_type: Document type (e.g., "report", "social", "code")

        Returns:
            Default profile name

        Raises:
            ValueError: If document type has no default
        """
        doc_defaults = self.defaults.get("document_types", {})
        if doc_type not in doc_defaults:
            available = ", ".join(doc_defaults.keys())
            raise ValueError(
                f"No default profile for document type '{doc_type}'. Available types: {available}"
            )
        return doc_defaults[doc_type]

    def get_api_key(self) -> str:
        """
        Get Gemini API key from environment.

        Returns:
            API key

        Raises:
            ValueError: If API key not configured
        """
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not set. Please configure it in .env file."
            )
        return api_key

    def get_output_dir(self) -> Path:
        """Get output directory, creating if necessary."""
        output_dir = Path(os.getenv("OUTPUT_DIR", "./output"))
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir

    def get_logs_dir(self) -> Path:
        """Get logs directory, creating if necessary."""
        logs_dir = Path(os.getenv("LOGS_DIR", "./logs"))
        logs_dir.mkdir(parents=True, exist_ok=True)
        return logs_dir

    def list_tone_profiles(self) -> Dict[str, str]:
        """
        List all available tone profiles with descriptions.

        Returns:
            Dictionary of profile names and descriptions
        """
        return {
            name: profile.get("description", "No description")
            for name, profile in self.tone_profiles.items()
        }

    def list_document_types(self) -> Dict[str, str]:
        """
        List all available document types and their default profiles.

        Returns:
            Dictionary of document types and default profiles
        """
        return self.defaults.get("document_types", {})
