# Change extension of this file from ".sample.py" to ".py" when using

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's3cret$tr1ng123456'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'testdb',
        'USER': 'testuser',
        'PASSWORD': 't3stpa$$w0rd',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST': {
            'NAME': 'testdb',
        },
    }
}

STRIPE = {
    'PUBLISHABLE_KEY': 'pk_test_XXXXXX',
    'SECRET_KEY': 'sk_test_XXXXXX',
}

CELERY_BROKER_URL = 'amqp://XXXXXX'

AWS_S3_ACCESS_KEY_ID = 'AKIAXXXXXX'
AWS_S3_SECRET_ACCESS_KEY = 'XXXXXX'
AWS_S3_REGION_NAME = 'eu-central-1'
AWS_S3_BUCKET_NAME = 'XXXXXX'
