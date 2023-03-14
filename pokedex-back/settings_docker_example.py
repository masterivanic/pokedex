##############################
# PARTIE SYSADMIN overriding
##############################
import django_env_overrides

DEBUG = False

STATIC_ROOT = "/var/www/static"
STATIC_URL = "/static/"

django_env_overrides.apply_to(globals())

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": POSTGRES_HOST,
        "NAME": "pokedex",
        "USER": "postgres",
        "PASSWORD": "8Fny?aXEFkh9ePA3",
        "PORT": POSTGRES_PORT,
    }
}
