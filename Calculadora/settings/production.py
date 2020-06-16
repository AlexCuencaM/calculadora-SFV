from .base import * 
# Base
SECRET_KEY = env('DJANGO_SECRET_KEY')
DATABASES ={
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}
ALLOWED_HOSTS = ['https://calculadora-sfv.herokuapp.com']

CORS_ORIGIN_WHITELIST = (
    'https://calculadora-sfv.herokuapp.com',
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

django_heroku.settings(locals())