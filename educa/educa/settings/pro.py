from .base import *

DEBUG = False

ADMINS = (
    ('ch1huizong', 'ch1huizong@gmail.com'),
)

ALLOWED_HOSTS = [
    '127.0.0.1',
    'educaproject.com',
    'www.educaproject.com',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'educa',
        'HOST': '192.168.1.10',
        'USER': 'educa',
        'PASSWORD': '1234test',
    }
}

SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
