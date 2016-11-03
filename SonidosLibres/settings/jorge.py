from .common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(PROJECT_PACKAGE.joinpath('db.sqlite3'))
    }
}

# DATABASES['default'] = dj_database_url.config(default=
# 'postgres://zertnrertjrkpu:F6VGxSDTh0T2lRbF0VMuH8yw90@ec2-23-23-226-41.compute-1.amazonaws.com:5432/dcvg9knc472ku')
