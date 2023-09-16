from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-0a*4rs!%5k=ix*$_o*e&nb8+n7_y99cf$+md^2za-tg+=y!uq@"

#ALLOWED_HOSTS = ["*"]
ALLOWED_HOSTS = [".vercel.app"]


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
#        'PASSWORD': "12345",
#        'HOST':  "localhost",
#        'PORT':  "5432",
#
#    }
#}



#Uncomment the following line to use DEBUG=True in production
#CSRF_TRUSTED_ORIGINS = ['https://apitraktordetal.demodev.click']


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
