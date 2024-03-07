import os
from .base import *  # NOQA


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY") or 'django-insecure-5u!jwom8i@m=*kgoy&*gr_g!h+ij8e80^&8(=5!^%!(8c2hqy8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost"]