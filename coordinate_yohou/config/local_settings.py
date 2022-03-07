import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'coordinate_yohou',
        'USER': 'postgres',
        'PASSWORD': 'Vio#lin01',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

ALLOWED_HOSTS = ['127.0.0.1:8000/']

DEBUG = True
