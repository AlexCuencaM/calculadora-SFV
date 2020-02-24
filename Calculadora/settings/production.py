from .base import * 
# Base
SECRET_KEY = env('DJANGO_SECRET_KEY')

DATABASES ={
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

CORS_ORIGIN_WHITELIST = (
    'https://calculadora-sfv.herokuapp.com:8000',
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

django_heroku.settings(locals())
