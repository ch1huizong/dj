from .base import *

import os
import sys

DEBUG = False

ADMINS = (("ch1huizong", "ch1huizong@gmail.com"),)

allowed_hosts = os.get('ALLOWED_HOSTS')
if allowed_hosts:
    ALLOWED_HOSTS = allowed_hosts.split(",")
else:
    print("ERROR ! Please Input ALLOWED_HOSTS env settings !")
    sys.exit(1)

db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

if db_host and db_name and db_user and db_password:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": db_name,
            "HOST": db_host,
            "USER": db_user,
            "PASSWORD": db_password,
        }
    }
else:
    print("ERROR ! Check DB SETTINGS !")
    sys.exit(1)

SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
