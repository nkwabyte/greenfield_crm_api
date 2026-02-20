from pathlib import Path
import os
from dotenv import load_dotenv
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables
load_dotenv(BASE_DIR / '.env')

# Application definition
INSTALLED_APPS = [
    # Unfold Admin Theme Apps
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'unfold.contrib.inlines',
    'unfold.contrib.import_export',
    'unfold.contrib.guardian',
    'unfold.contrib.simple_history',
    # 'unfold.contrib.location_field',  # optional, if django-location-field package is used
    # 'unfold.contrib.constance',  # optional, if django-constance package is used

    # Default Django APPS
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party APPS
    'rest_framework',
    'corsheaders',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'django_ratelimit',
    'simple_history',
    'csp',

    # Local Apps
    'core.apps.CoreConfig',
    'accounts.apps.AccountsConfig',
    'farmers.apps.FarmersConfig',
    'inventory.apps.InventoryConfig',
    'finances.apps.FinancesConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # CUSTOM MIDDLEWARE
    'simple_history.middleware.HistoryRequestMiddleware',
    'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'api.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Supabase Auth Integration
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY')
SUPABASE_JWT_SECRET = os.environ.get('SUPABASE_JWT_SECRET')

# Django REST Framework Settings
REST_FRAMEWORK = {
    # 1. Custom Supabase Authentication
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'accounts.authentication.supabase.SupabaseJWTAuthentication',
        'rest_framework.authentication.SessionAuthentication', # Useful for the browsable API
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    
    # 2. Schema Generation
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    # 3. Global Pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
    
    # 4. Global Filtering, Searching, and Ordering
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'SEARCH_PARAM': 'search',
}

# SPECTACULAR SETTINGS
SPECTACULAR_SETTINGS = {
    'TITLE': 'Greenfield CRM API',
    'DESCRIPTION': 'Modular Django API integrating with Supabase to manage agriculture operations.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR', 
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
}

# Caching
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Content Security Policy
CONTENT_SECURITY_POLICY = {
    'DIRECTIVES': {
        'block-all-mixed-content': True,
        'connect-src': ("'self'",),
        'default-src': ("'none'",),
        'font-src': ("'self'", "https:", "data:"),
        'frame-ancestors': ("'none'",),
        'img-src': ("'self'", "data:", "https:"),
        'script-src': ("'self'", "'unsafe-inline'"),
        'style-src': ("'self'", "'unsafe-inline'", "https:"),
    }
}

# Rate Limiting
RATELIMIT_ENABLE = True
RATELIMIT_GROUP_PREFIX = 'ratelimit'
RATELIMIT_KEY_PREFIX = 'rl'
RATELIMIT_USE_CACHE = 'default'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}

# Unfold Admin Theme Configuration
UNFOLD = {
    "SITE_TITLE": "Greenfield CRM Admin",
    "SITE_HEADER": "Greenfield CRM",
    "SITE_URL": "/",
    "LOGIN": {
        "image": "https://images.unsplash.com/photo-1592982537447-6f233496bc35?q=80&w=2940&auto=format&fit=crop", 
    },
    "show_theme_switch": True,
    "STYLES": [
        "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap",
    ],
    "COLORS": {
        "primary": {
            "50": "240 253 244",
            "100": "220 252 231",
            "200": "187 247 208",
            "300": "134 239 172",
            "400": "74 222 128",
            "500": "34 197 94",
            "600": "22 163 74",
            "700": "21 128 61",
            "800": "22 101 52",
            "900": "20 83 45",
            "950": "5 46 22",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "navigation": [
            {
                "title": "Dashboard",
                "icon": "dashboard",
                "link": reverse_lazy("admin:index"),
            },
            {
                "title": "Accounts",
                "icon": "person",
                "items": [
                    {
                        "title": "Users",
                        "link": reverse_lazy("admin:accounts_user_changelist"),
                    },
                    {
                        "title": "Employee Profiles",
                        "link": reverse_lazy("admin:accounts_employeeprofile_changelist"),
                    },
                ],
            },
            {
                "title": "Farmers",
                "icon": "agriculture",
                "items": [
                    {
                        "title": "Farmers",
                        "link": reverse_lazy("admin:farmers_farmer_changelist"),
                    },
                    {
                        "title": "Farmer Groups",
                        "link": reverse_lazy("admin:farmers_farmergroup_changelist"),
                    },
                    {
                        "title": "Requests",
                        "link": reverse_lazy("admin:farmers_farmerrequest_changelist"),
                    },
                ],
            },
            {
                "title": "Inventory",
                "icon": "inventory_2",
                "items": [
                    {
                        "title": "Products",
                        "link": reverse_lazy("admin:inventory_product_changelist"),
                    },
                    {
                        "title": "Suppliers",
                        "link": reverse_lazy("admin:inventory_supplier_changelist"),
                    },
                ],
            },
            {
                "title": "Finances",
                "icon": "payments",
                "items": [
                    {
                        "title": "Transactions",
                        "link": reverse_lazy("admin:finances_transaction_changelist"),
                    },
                ],
            },
        ],
    },
}
