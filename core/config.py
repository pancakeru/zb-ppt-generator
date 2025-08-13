# core/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env in dev; in Docker/Cloud use platform env vars
load_dotenv(override=False)

ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT / "assets"
TEMPLATES_DIR = ASSETS_DIR / "templates"
PPT_TEMPLATE_PATH = TEMPLATES_DIR / "Riot Games PPT Template.pptx"

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
HEADLESS = os.getenv("HEADLESS", "1") == "1"