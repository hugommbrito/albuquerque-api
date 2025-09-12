"""
WSGI config for abqApiProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

BASE_DIR = Path(__file__).resolve().parents[1]
# Ensure the parent directory (which contains the abqApiProject package) is on sys.path
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abqApiProject.settings')

# Expose both names for compatibility with Django and Vercel
application = get_wsgi_application()
app = application  # Vercel looks for `app`
