from .base import *

DEBUG = False

ALLOWED_HOSTS = [
        '.dianarice.art',
        '45.56.110.221',
        'static.dianarice.art',
        'media.dianarice.art'
        ]

with open('/usr/local/secret/dianarice/secretkey.txt') as f:
    SECRET_KEY = f.read().strip()

try:
    from .local import *
except ImportError:
    pass

#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'handlers': {
#        'file': {
#            'level': 'DEBUG',
#            'class': 'logging.FileHandler',
#            'filename': '/var/www/webapps/dianarice/log/django/debug.log',
#        },
#    },
#    'loggers': {
#        'django': {
#            'handlers': ['file'],
#            'level': 'DEBUG',
#            'propagate': True,
#        },
#    },
#}
