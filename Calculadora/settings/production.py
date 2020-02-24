from .base import * 
# Base
SECRET_KEY = '5=lchar9e*pz(3mt-xsj8l$$pe4-4(j)i)kt-hlhi4m5ukt2#3'

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
