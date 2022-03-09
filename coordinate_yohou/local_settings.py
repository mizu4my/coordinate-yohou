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

SECRET_KEY = 'django-insecure-8i9s-4*=4m$k^2o47tu=zx7*(6&%rxw=+dfh*3jn8g@l4fo-y-'

ALLOWED_HOSTS = ['127.0.0.1']

DEBUG = True
