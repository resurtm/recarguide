# Change extension of this file from "*.sample.py" to "*.py" when using

import os

import raven

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'somedbname',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'TEST': {
            'NAME': 'somedbname_test',
        },
    }
}

INSTALLED_APPS = []

STRIPE = {
    'PUBLISHABLE_KEY': 'pk_test_XXXXXX',
    'SECRET_KEY': 'sk_test_XXXXXX',
}

CELERY_BROKER_URL = 'amqp://XXXXXX'

AWS_S3_ACCESS_KEY_ID = 'AKIAXXXXXX'
AWS_S3_SECRET_ACCESS_KEY = 'XXXXXX'
AWS_S3_REGION_NAME = 'eu-central-1'
AWS_S3_BUCKET_NAME = 'XXXXXX'

RAVEN_CONFIG = {
    'dsn': 'https://XXX',
    'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}
