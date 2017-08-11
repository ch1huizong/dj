from .base import *


DEBUG = False

ADMINS = (
    ('che', 'chehuizong@163.com'),
)

ALLOWED_HOSTS = ['educa.com', 'www.educa.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'educa',
        'USER': 'educa',
        'PASSWORD': '1234test',
    }
}
