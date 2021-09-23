from os.path import abspath, dirname, join
import sys
import django
from django.conf import settings
from django.core import management

sys.path.insert(0, '.')

settings.configure(
    BASE_DIR = dirname(abspath(__file__)),
    DEBUG=True,
    ROOT_URLCONF = "banjo.urls",
    DATABASES = {
        "default": {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'database.sqlite',
        }
    },
    DEFAULT_AUTO_FIELD = 'django.db.models.AutoField',
    ALLOWED_HOSTS = "*",
    SECRET_KEY = "xxx",
    INSTALLED_APPS = [
        "django_extensions",
        "banjo",
        "app",
    ],
    SHELL_PLUS_DONT_LOAD = [
        "banjo",
    ]
)
django.setup()

def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-s", "--shell", action="store_true")
    parser.add_argument("-p", "--port", type=int, default=5000)
    args = parser.parse_args()

    from app import views
    management.execute_from_command_line(['', 'makemigrations', 'app', 'banjo'])
    management.execute_from_command_line(['', 'migrate'])
    
    if args.shell:
        management.execute_from_command_line(['', 'shell_plus'])
    else:
        management.execute_from_command_line(['', 'runserver', str(args.port)])
