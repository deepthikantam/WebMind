import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if present
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

ANAKIN_API_KEY = os.getenv("ANAKIN_API_KEY", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
ACTION_WEBHOOK_URL = os.getenv("ACTION_WEBHOOK_URL", "").strip()

def get_anakin_key() -> str:
    """Return configured Anakin API key or fallback to env."""
    return os.getenv("ANAKIN_API_KEY", "").strip()

def get_gemini_key() -> str:
    """Return configured Gemini API key or fallback to env."""
    return os.getenv("GEMINI_API_KEY", "").strip()

def is_configured() -> dict[str, bool]:
    """Check configuration status of required services."""
    return {
        "anakin": bool(get_anakin_key()),
        "gemini": bool(get_gemini_key()),
        "webhook": bool(os.getenv("ACTION_WEBHOOK_URL", "").strip())
    }
