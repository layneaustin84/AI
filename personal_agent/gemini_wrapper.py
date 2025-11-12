"""
Gemini API Wrapper for Personal Agent
Handles all interactions with Google's Gemini API
"""

import os
import json
import logging
from typing import Optional, Dict, Any
import requests

logger = logging.getLogger(__name__)


class GeminiWrapper:
    """Wrapper around Google Gemini API for safe, consistent access."""

    def __init__(self, api_key: str):
        """
        Initialize Gemini wrapper with API key.

        Args:
            api_key: Google Gemini API key
        """
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2-5-flash:generateContent"
        self.model = "gemini-2-5-flash"

    def humanize_text(
        self,
        text: str,
        tone_profile: Dict[str, Any],
        custom_instruction: Optional[str] = None
    ) -> str:
        """
        Humanize text using specified tone profile.

        Args:
            text: Text to humanize
            tone_profile: Dictionary containing tone profile with 'system_prompt'
            custom_instruction: Optional additional instruction to append

        Returns:
            Humanized text

        Raises:
            ValueError: If API call fails
        """
        system_prompt = tone_profile.get("system_prompt", "Rewrite the following text to be more human and engaging.")

        if custom_instruction:
            system_prompt += f"\n\nAdditional instruction: {custom_instruction}"

        full_prompt = f"{system_prompt}\n\nText to rewrite:\n{text}"

        return self._call_gemini(full_prompt)

    def summarize_text(self, text: str) -> str:
        """
        Summarize text to key points.

        Args:
            text: Text to summarize

        Returns:
            Summary
        """
        prompt = f"Provide a concise summary of the following text, highlighting the key points:\n\n{text}"
        return self._call_gemini(prompt)

    def extract_takeaways(self, text: str) -> str:
        """
        Extract key takeaways from text.

        Args:
            text: Text to extract from

        Returns:
            Bulleted list of key takeaways
        """
        prompt = f"Extract the key takeaways from the following text as a bulleted list:\n\n{text}"
        return self._call_gemini(prompt)

    def change_tone(self, text: str, target_tone: str) -> str:
        """
        Rewrite text in a different tone.

        Args:
            text: Text to rewrite
            target_tone: Target tone (e.g., "casual", "formal", "technical")

        Returns:
            Rewritten text
        """
        prompt = f"Rewrite the following text in a {target_tone} tone:\n\n{text}"
        return self._call_gemini(prompt)

    def _call_gemini(self, prompt: str) -> str:
        """
        Make a call to Gemini API.

        Args:
            prompt: The prompt to send to Gemini

        Returns:
            Generated text response

        Raises:
            ValueError: If API call fails
        """
        try:
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ]
            }

            headers = {
                "Content-Type": "application/json"
            }

            params = {
                "key": self.api_key
            }

            response = requests.post(
                self.base_url,
                json=payload,
                headers=headers,
                params=params,
                timeout=30
            )

            if response.status_code != 200:
                error_msg = response.text
                logger.error(f"Gemini API error: {response.status_code} - {error_msg}")
                raise ValueError(f"Gemini API error: {response.status_code}")

            data = response.json()

            # Extract text from response
            if "candidates" in data and len(data["candidates"]) > 0:
                candidate = data["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    if len(candidate["content"]["parts"]) > 0:
                        return candidate["content"]["parts"][0].get("text", "")

            raise ValueError("Unexpected Gemini API response format")

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error calling Gemini API: {e}")
            raise ValueError(f"Failed to call Gemini API: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error from Gemini API: {e}")
            raise ValueError(f"Invalid response from Gemini API: {e}")
