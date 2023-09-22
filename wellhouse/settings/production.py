from .base import *

DEBUG = False

SECRET_KEY = "django-insecure-0a*4rs!%5k=ix*$_o*e&nb8+n7_y99cf$+md^2za-tg+=y!uq@"

# ALLOWED_HOSTS = ["apiwellhouse.demodev.click", "www.apiwellhouse.demodev.click"]
ALLOWED_HOSTS = ["*"]


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply@traktordetal.com'
EMAIL_HOST_PASSWORD = 'JdDz9bxPCdsqEqua8fSV'

DEFAULT_FROM_EMAIL = 'noreply@traktordetal.com'
#EMAIL_HOST_USER = 'zekiyev014@gmail.com'
EMAIL_HOST_USER = 'noreply@traktordetal.com'

WAGTAILFRONTENDCACHE = {
    'cloudflare': {
        'BACKEND': 'wagtail.contrib.frontend_cache.backends.CloudflareBackend',
        'EMAIL': 'developer.medium@gmail.com',
        'API_KEY': 'UHZztbLtqeoV8jepG4B49mnOTq7d0yQeAcGxdAGl',
        'ZONEID': '17e99bef0deaeb4e0767eedb334cfadc',
    },
}

#after completing project you must uncomment this CACHES variable

#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#        'LOCATION': os.path.join(BASE_DIR, 'cache'),
#        'KEY_PREFIX': 'wagtailcache',
#        'TIMEOUT': 31536000, # one hour (in seconds)
#    },
#
#}


#for disabling cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':  "wellhouse",
        'USER':  "wellhouse_user",
        'PASSWORD': "6RpIuYMcxArKD47EP9fjANze25eP5e2gJdWrhrriq7",
#        'HOST':  "localhost",
#        'HOST':  "167.235.240.205",
        'HOST':  "95.216.217.57",
        'PORT':  "5432",

    }
}


COMPRESS_OFFLINE = True

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_CSS_HASHING_METHOD = 'content'

CORS_ORIGIN_ALLOW_ALL = True

CSRF_TRUSTED_ORIGINS = ['https://apiwellhouse.demodev.click', 'https://well-houses.com']

CSRF_COOKIE_NAME = 'csrftoken'

CORS_ALLOWED_ORIGINS = [
    "https://apiwellhouse.demodev.click",
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',  # Include OPTIONS method
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'Accept',
    'Accept-Encoding',
    'Authorization',
    'Content-Type',
    'Origin',
    'X-CSRFToken',  # Include any custom headers you're using
]




#STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
#STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = 'AKIAV72G2P4PSHT2PJVC'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'wellhouses'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False



STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
# STATICFILES_DIRS = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"



WAGTAILADMIN_BASE_URL = ALLOWED_HOSTS



try:
    from .local import *
except ImportError:
    pass

