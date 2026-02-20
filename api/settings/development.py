from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-hn$zbol#%79ofvgzljuzl8a7ip5mj5xlx!$2t@i&z+3vrkdqru')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# Default: local PostgreSQL (development-safe, isolated from production).
# Override: set USE_SUPABASE_DB=true in .env to connect to Supabase directly via DATABASE_URL.
from urllib.parse import urlparse

_use_supabase = os.environ.get('USE_SUPABASE_DB', 'false').lower() == 'true'
_db_url = os.environ.get('DATABASE_URL')

if _use_supabase and _db_url:
    _u = urlparse(_db_url)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": _u.path.lstrip("/"),
            "USER": _u.username,
            "PASSWORD": _u.password,
            "HOST": _u.hostname,
            "PORT": str(_u.port or 5432),
            "OPTIONS": {"sslmode": "require"},
        }
    }
else:
    # Local PostgreSQL — default for development.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", "greenfield_crm"),
            "USER": os.getenv("DB_USER", "postgres"),
            "PASSWORD": os.getenv("DB_PASSWORD", "admin"),
            "HOST": os.getenv("DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }

# CORS
CORS_ALLOW_ALL_ORIGINS = True
