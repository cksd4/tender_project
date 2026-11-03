import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

# Extract variables from local .env environment profile
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Allow localized hosting alongside generic production domains
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.herokuapp.com',] 
ROOT_URLCONF = 'tender_project.urls'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'catering', # Register your custom catering app
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Route system authentication processing to your custom user table profiles
AUTH_USER_MODEL = 'catering.UserProfile'
AUTHENTICATION_BACKENDS = ['catering.auth_backends.EmailBackend']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True, # Permits discovery of application directory templates
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'catering.context_processors.session_timeout',
            ],
        },
    },
]

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Heroku Database Routing Configuration Layer
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

# WhiteNoise Storage Optimization Engine for external stylesheets
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

 #Force the active session to expire completely when the user closes their browser
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# If a user is inactive for this long, Django flushes their authentication token data.
SESSION_COOKIE_AGE = 1800  # 30 minutes in seconds

# Automatically refresh the expiration countdown timer every time the user clicks a page
SESSION_SAVE_EVERY_REQUEST = True

# Automatic post-authentication routing redirects
LOGIN_URL = 'employee_login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'employee_login'

# Uses the console backend for absolute simplicity during evaluation.
# Reset links will display inside your VS Code terminal running the server.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'