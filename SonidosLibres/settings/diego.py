from .common import *  # noqa
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'SonidosLibres',
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# DATABASES['default'] = dj_database_url.config(default='postgres://zertnrertjrkpu:F6VGxSDTh0T2lRbF0VMuH8yw90@ec2-23-23-226-41.compute-1.amazonaws.com:5432/dcvg9knc472ku')
