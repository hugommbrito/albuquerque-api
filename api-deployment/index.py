import os
import sys
from pathlib import Path

# Ensure the Django project (inside "abq-api") is importable
REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT_DIR = REPO_ROOT / 'abq-api'
if str(PROJECT_DIR) not in sys.path:
    sys.path.append(str(PROJECT_DIR))

# Point Django to the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abqApiProject.settings')

# Import the WSGI app exposed by the project
from abqApiProject.wsgi import app  # noqa: E402,F401

