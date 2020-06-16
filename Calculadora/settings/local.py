"""Development settings."""
from .base import *
DEBUG = True
SECRET_KEY = env('DJANGO_SECRET_KEY', default='5=lchar9e*pz(3mt-xsj8l$$pe4-4(j)i)kt-hlhi4m5ukt2#3')
ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0',]
# Database MySQL
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
# settings.py
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'OPTIONS': {
#             'read_default_file': os.path.join(ROOT_DIR, 'my.cnf'),
#              'init_command': 'SET default_storage_engine=INNODB',
#         },
#     }
# }
CORS_ORIGIN_WHITELIST = (
    'https://127.0.0.1:8000',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'calculadora',
        'USER': 'alex',
        'PASSWORD': 'test',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG