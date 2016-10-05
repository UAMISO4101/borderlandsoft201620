from .common import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(PROJECT_PACKAGE.joinpath('db.sqlite3')),  # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'NAME': 'dcvg9knc472ku',
        # 'USER': os.environ['POSTGRES_USER'],
        # 'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        # 'HOST': 'ec2-23-23-226-41.compute-1.amazonaws.com',
        # 'PORT': '5432',
    }
}

# DATABASES['default'] = dj_database_url.config(default='postgres://zertnrertjrkpu:F6VGxSDTh0T2lRbF0VMuH8yw90@ec2-23-23-226-41.compute-1.amazonaws.com:5432/dcvg9knc472ku')
