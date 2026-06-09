from pathlib import Path
import json

SESSION_DIR = Path("session")
SETTINGS_FILE = SESSION_DIR / "settings.json"

DEFAULT_SETTINGS = {
    "llm_provider": "google",
    "llm_model": "gemini-3.1-flash-lite",
    "embedding_model": "embeddinggemma",
    "google_api_key": "",
    "hf_token": "",
    "language": "English",
    "db_name": "0",
    "is_processed": False,
}

def initialize_session():
    """Ensure session directory and default settings file exist."""
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    
    if not SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_SETTINGS, f, indent=2)

def load_settings():
    """Load settings from file, creating defaults if needed."""
    initialize_session()   # safe – no recursion now
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_settings(settings):
    """Save settings dict to file."""
    SESSION_DIR.mkdir(parents=True, exist_ok=True)   # ensure directory exists
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)
    # DO NOT call initialize_session() here