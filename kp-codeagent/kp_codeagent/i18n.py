"""Internationalization support for KP Code Agent."""

import os
import json
from pathlib import Path
from typing import Dict, Any

# Default language
DEFAULT_LANG = "en"

# Supported languages
SUPPORTED_LANGUAGES = ["en", "es"]


class I18n:
    """Handle translations for KP Code Agent."""

    def __init__(self, lang: str = None):
        """Initialize with a specific language."""
        self.lang = lang or self._detect_language()
        self.translations = self._load_translations()

    def _detect_language(self) -> str:
        """Detect system language."""
        # Check environment variables
        lang = os.getenv("KP_LANG") or os.getenv("LANG", "")

        # Extract language code (e.g., 'es_MX' -> 'es')
        if lang.startswith("es"):
            return "es"
        else:
            return "en"

    def _load_translations(self) -> Dict[str, Any]:
        """Load translation file for the current language."""
        translations_dir = Path(__file__).parent / "translations"
        translation_file = translations_dir / f"{self.lang}.json"

        if not translation_file.exists():
            # Fallback to English
            translation_file = translations_dir / "en.json"

        try:
            with open(translation_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            # Return empty dict if loading fails
            return {}

    def t(self, key: str, **kwargs) -> str:
        """
        Translate a key with optional formatting.

        Args:
            key: Translation key (e.g., 'welcome.title')
            **kwargs: Format variables

        Returns:
            Translated and formatted string
        """
        # Navigate nested dictionary using dot notation
        keys = key.split('.')
        value = self.translations

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, key)
            else:
                return key

        # If value is still a dict, return the key
        if isinstance(value, dict):
            return key

        # Format with kwargs if provided
        if kwargs:
            try:
                return value.format(**kwargs)
            except (KeyError, ValueError):
                return value

        return value

    def set_language(self, lang: str):
        """Change the current language."""
        if lang in SUPPORTED_LANGUAGES:
            self.lang = lang
            self.translations = self._load_translations()


# Global instance
_i18n_instance = None


def get_i18n(lang: str = None) -> I18n:
    """Get or create the global i18n instance."""
    global _i18n_instance
    if _i18n_instance is None or lang is not None:
        _i18n_instance = I18n(lang)
    return _i18n_instance


def t(key: str, **kwargs) -> str:
    """Shortcut for translation."""
    return get_i18n().t(key, **kwargs)
