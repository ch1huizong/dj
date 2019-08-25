from .base import *

DEBUG = False

ADMINS = (
    ('ch1huizong', 'ch1huizong@gmail.com'),
)

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'educa',
        'HOST': '192.168.1.10',
        'USER': 'educa1',
        'PASSWORD': '1234test',
    }
}
