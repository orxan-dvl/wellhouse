from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-0a*4rs!%5k=ix*$_o*e&nb8+n7_y99cf$+md^2za-tg+=y!uq@"

#ALLOWED_HOSTS = ["*"]


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME':  "wellhouse",
#        'USER':  "wellhouse_user",
#        'PASSWORD': "6RpIuYMcxArKD47EP9fjANze25eP5e2gJdWrhrriq7",
##        'HOST':  "localhost",
##        'HOST':  "167.235.240.205",
#        'HOST':  "95.216.217.57",
#        'PORT':  "5432",
#
#    }
#}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME':  "wellhouse",
#        'USER':  "wellhouse_user",
#        'PASSWORD': "12345",
#        'HOST':  "localhost",
#        'PORT':  "5432",
#
#    }
#}



#Uncomment the following line to use DEBUG=True in production
#CSRF_TRUSTED_ORIGINS = ['https://apiwellhouse.demodev.click']


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply@traktordetal.com'
EMAIL_HOST_PASSWORD = 'JdDz9bxPCdsqEqua8fSV'

DEFAULT_FROM_EMAIL = 'noreply@traktordetal.com'
#EMAIL_HOST_USER = 'zekiyev014@gmail.com'
EMAIL_HOST_USER = 'noreply@traktordetal.com'

try:
    from .local import *
except ImportError:
    pass


CORS_ORIGIN_ALLOW_ALL = True
















CORS_ORIGIN = [
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "POST",
            "GET",
            "PUT"
        ],
        "AllowedOrigins": [
            "*"
        ]
    }
]