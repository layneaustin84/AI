"""
File Handler for Personal Agent
Handles file operations, versioning, and operation logging
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class FileHandler:
    """Handles file operations and version logging."""

    def __init__(self, config):
        """
        Initialize file handler.

        Args:
            config: ConfigLoader instance
        """
        self.config = config
        self.logs_dir = config.get_logs_dir()
        self.output_dir = config.get_output_dir()
        self._init_logs()

    def _init_logs(self) -> None:
        """Initialize log files if they don't exist."""
        self.operations_log = self.logs_dir / "operations.jsonl"
        if not self.operations_log.exists():
            self.operations_log.touch()
            logger.info(f"Created operations log at {self.operations_log}")

    def log_operation(
        self,
        operation: str,
        input_length: int,
        output_length: int,
        tone_profile: str,
        doc_type: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log an operation to the operations log.

        Args:
            operation: Operation type (e.g., "humanize", "summarize")
            input_length: Length of input text
            output_length: Length of output text
            tone_profile: Tone profile used
            doc_type: Document type (optional)
            metadata: Additional metadata (optional)
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "input_length": input_length,
            "output_length": output_length,
            "tone_profile": tone_profile,
            "doc_type": doc_type,
            "metadata": metadata or {}
        }

        try:
            with open(self.operations_log, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            logger.info(f"Logged operation: {operation}")
        except IOError as e:
            logger.error(f"Failed to log operation: {e}")

    def get_operation_history(self, limit: int = 50) -> list:
        """
        Get recent operation history.

        Args:
            limit: Maximum number of entries to return

        Returns:
            List of operation log entries
        """
        entries = []
        try:
            with open(self.operations_log, 'r') as f:
                for line in f:
                    if line.strip():
                        entries.append(json.loads(line))
            return entries[-limit:]
        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Failed to read operation history: {e}")
            return []

    def save_text_version(
        self,
        filename: str,
        text: str,
        version_type: str = "output"
    ) -> Path:
        """
        Save a text version with timestamp.

        Args:
            filename: Base filename (without extension)
            text: Text content to save
            version_type: Type of version (e.g., "output", "draft", "final")

        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"{filename}_{version_type}_{timestamp}.txt"
        output_path = self.output_dir / output_name

        try:
            output_path.write_text(text)
            logger.info(f"Saved text version: {output_path}")
            return output_path
        except IOError as e:
            logger.error(f"Failed to save text version: {e}")
            raise

    def load_text_file(self, filepath: str) -> str:
        """
        Load text from a file.

        Args:
            filepath: Path to file

        Returns:
            File contents

        Raises:
            FileNotFoundError: If file doesn't exist
            IOError: If file can't be read
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        try:
            return path.read_text()
        except IOError as e:
            logger.error(f"Failed to read file {filepath}: {e}")
            raise

    def get_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics from operation history.

        Returns:
            Dictionary with statistics
        """
        history = self.get_operation_history(limit=None)

        if not history:
            return {
                "total_operations": 0,
                "avg_input_length": 0,
                "avg_output_length": 0,
                "compression_ratio": 0
            }

        total_input = sum(h.get("input_length", 0) for h in history)
        total_output = sum(h.get("output_length", 0) for h in history)

        return {
            "total_operations": len(history),
            "avg_input_length": total_input // len(history) if history else 0,
            "avg_output_length": total_output // len(history) if history else 0,
            "compression_ratio": round(total_output / total_input, 2) if total_input > 0 else 0,
            "last_operation": history[-1].get("timestamp") if history else None
        }
