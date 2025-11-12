"""
Service layer for Personal Agent
Wraps CLI modules (gemini_wrapper, config_loader, file_handler) for API access
"""

import sys
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Add personal_agent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "personal_agent"))

from config_loader import ConfigLoader
from gemini_wrapper import GeminiWrapper
from file_handler import FileHandler

logger = logging.getLogger(__name__)


class PersonalAgentService:
    """Service class for Personal Agent operations."""

    _instance = None
    _initialized = False

    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the service (only once)."""
        if self._initialized:
            return

        try:
            self.config = ConfigLoader()
            self.gemini = GeminiWrapper(self.config.get_api_key())
            self.file_handler = FileHandler(self.config)
            self._initialized = True
            logger.info("✅ PersonalAgentService initialized")
        except Exception as e:
            logger.error(f"Failed to initialize PersonalAgentService: {e}")
            raise

    def humanize_text(
        self,
        text: str,
        tone: str,
        doc_type: Optional[str] = None,
        instruction: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Humanize text using specified tone profile.

        Args:
            text: Text to humanize
            tone: Tone profile name
            doc_type: Document type (optional)
            instruction: Custom instruction (optional)

        Returns:
            Dictionary with original, humanized, and metadata
        """
        try:
            # Get tone profile
            if tone and tone in self.config.tone_profiles:
                profile = self.config.get_tone_profile(tone)
            elif doc_type:
                default_tone = self.config.get_default_profile_for_type(doc_type)
                profile = self.config.get_tone_profile(default_tone)
                tone = default_tone
            else:
                profile = self.config.get_tone_profile("friendly")
                tone = "friendly"

            # Humanize
            humanized = self.gemini.humanize_text(text, profile, instruction)

            # Log operation
            self.file_handler.log_operation(
                operation="humanize",
                input_length=len(text),
                output_length=len(humanized),
                tone_profile=tone,
                doc_type=doc_type,
                metadata={"instruction": bool(instruction)}
            )

            return {
                "original": text,
                "humanized": humanized,
                "tone": tone,
                "input_length": len(text),
                "output_length": len(humanized),
                "timestamp": datetime.now()
            }

        except ValueError as e:
            logger.error(f"Humanize error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in humanize: {e}")
            raise

    def summarize_text(self, text: str) -> Dict[str, Any]:
        """
        Summarize text.

        Args:
            text: Text to summarize

        Returns:
            Dictionary with original, summary, and metadata
        """
        try:
            summary = self.gemini.summarize_text(text)

            self.file_handler.log_operation(
                operation="summarize",
                input_length=len(text),
                output_length=len(summary),
                tone_profile="N/A",
                doc_type=None
            )

            return {
                "original": text,
                "summary": summary,
                "input_length": len(text),
                "output_length": len(summary),
                "timestamp": datetime.now()
            }

        except Exception as e:
            logger.error(f"Summarize error: {e}")
            raise

    def extract_takeaways(self, text: str) -> Dict[str, Any]:
        """
        Extract key takeaways from text.

        Args:
            text: Text to extract from

        Returns:
            Dictionary with original, takeaways, and metadata
        """
        try:
            takeaways = self.gemini.extract_takeaways(text)

            self.file_handler.log_operation(
                operation="takeaways",
                input_length=len(text),
                output_length=len(takeaways),
                tone_profile="N/A",
                doc_type=None
            )

            return {
                "original": text,
                "takeaways": takeaways,
                "input_length": len(text),
                "output_length": len(takeaways),
                "timestamp": datetime.now()
            }

        except Exception as e:
            logger.error(f"Takeaways extraction error: {e}")
            raise

    def get_tone_profiles(self) -> Dict[str, Any]:
        """
        Get all available tone profiles.

        Returns:
            Dictionary of profiles
        """
        profiles = {}
        for name, profile in self.config.tone_profiles.items():
            profiles[name] = {
                "name": profile.get("name", name),
                "description": profile.get("description", ""),
                "tone_keywords": profile.get("tone_keywords", []),
                "use_cases": profile.get("use_cases", [])
            }
        return profiles

    def get_document_types(self) -> Dict[str, str]:
        """
        Get document types and their default profiles.

        Returns:
            Dictionary of document types
        """
        return self.config.list_document_types()

    def get_operation_history(self, limit: int = 50) -> list:
        """
        Get operation history.

        Args:
            limit: Maximum number of entries

        Returns:
            List of operation log entries
        """
        return self.file_handler.get_operation_history(limit=limit)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get usage statistics.

        Returns:
            Dictionary with statistics
        """
        return self.file_handler.get_stats()

    def batch_humanize(
        self,
        files: list,
        tone: str,
        doc_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Batch humanize multiple files.

        Args:
            files: List of file content dictionaries
            tone: Tone profile to use
            doc_type: Document type (optional)

        Returns:
            Dictionary with results
        """
        results = []
        successful = 0

        try:
            # Get tone profile
            if tone and tone in self.config.tone_profiles:
                profile = self.config.get_tone_profile(tone)
            elif doc_type:
                default_tone = self.config.get_default_profile_for_type(doc_type)
                profile = self.config.get_tone_profile(default_tone)
                tone = default_tone
            else:
                profile = self.config.get_tone_profile("friendly")
                tone = "friendly"

            for file_data in files:
                try:
                    text = file_data.get("content", "")
                    filename = file_data.get("filename", "unknown")

                    if not text:
                        results.append({
                            "filename": filename,
                            "status": "skipped",
                            "reason": "Empty file"
                        })
                        continue

                    humanized = self.gemini.humanize_text(text, profile)

                    self.file_handler.log_operation(
                        operation="humanize_batch",
                        input_length=len(text),
                        output_length=len(humanized),
                        tone_profile=tone,
                        doc_type=doc_type,
                        metadata={"filename": filename}
                    )

                    results.append({
                        "filename": filename,
                        "status": "success",
                        "input_length": len(text),
                        "output_length": len(humanized),
                        "humanized": humanized
                    })
                    successful += 1

                except Exception as e:
                    logger.error(f"Error processing {filename}: {e}")
                    results.append({
                        "filename": filename,
                        "status": "failed",
                        "error": str(e)
                    })

            return {
                "files_processed": len(files),
                "successful": successful,
                "failed": len(files) - successful,
                "results": results,
                "timestamp": datetime.now()
            }

        except Exception as e:
            logger.error(f"Batch humanize error: {e}")
            raise


# Singleton instance
_service = None


def get_service() -> PersonalAgentService:
    """Get or create service instance."""
    global _service
    if _service is None:
        _service = PersonalAgentService()
    return _service
