import os.path

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import colorama

class Command(BaseCommand):
    help = 'Reset the Webstack, remove database, .env and settings_customized.py file'

    def handle(self, *args, **options):
        if settings.DEBUG:
            paths = [".env", "db.sqlite3", "securitygroups/settings_customized.py", "celerybeat-schedule"]

            for path in paths:
                if os.path.exists(path):
                    os.remove(path)
                    print(f"{colorama.Fore.GREEN}The {colorama.Fore.RED}{path}{colorama.Fore.GREEN} file is {colorama.Fore.RED}removed.{colorama.Style.RESET_ALL}")
        else:
            print(f"{colorama.Fore.GREEN}Your are {colorama.Fore.RED}not{colorama.Style.RESET_ALL}{colorama.Fore.GREEN} on DEBUG mode. Unable to reset.{colorama.Style.RESET_ALL}")