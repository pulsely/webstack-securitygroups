import os, colorama, time, threading
import getpass
from django.core.management.utils import get_random_secret_key
from django.core.management import call_command

DEFAULT_FILE_TEXT = '''
DEBUG=true
ALLOWED_HOSTS="*"

AWS_EC2_SECURITY_GROUP="XXXXXXXXX"
AWS_REGION_SECURITY_GROUP="ap-northeast-1"

SERVER_PRODUCTION_HOSTNAME = "securitygroups.yourcompany.com"

EMAIL_BACKEND="django_ses.SESBackend"
AWS_SES_REGION_NAME="us-west-2"
AWS_SES_REGION_ENDPOINT="email.us-west-2.amazonaws.com"
SERVER_EMAIL="youremail@yourcompany.com"

'''

def create_default_file():
    '''
    # The file should be in the following format:
    DEBUG=true
    SECRET_KEY=""
    ALLOWED_HOSTS="*"
    DEFAULT_USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
    DEFAULT_PERIODIC_MINUTES=7
    '''

    SECRET_KEY = get_random_secret_key()

    f = open(".env", "w")
    f.write(f'SECRET_KEY="{SECRET_KEY}"')
    f.write("\n")

    f.write(DEFAULT_FILE_TEXT)
    f.close()

def create_first_user():
    if is_docker():
        print("Users are not created interactively as you are using docker. Please use the add super user link to add user.")
    else:
        from core.forms import AdminResetForm
        from core.models import ROLE_ADMIN
        from django.contrib.auth import get_user_model

        User = get_user_model()

        print(f"{colorama.Fore.RED}You do not have any user in the system yet.{colorama.Style.RESET_ALL}")
        print("Now, set the username and password of your superuser:")
        username = input("Username: ")

        flag_added = False

        while not flag_added:
            password = getpass.getpass("Password: ")
            f = AdminResetForm({ "password" : password })
            if f.is_valid():
                flag_added = True
            else:
                if f.errors:
                    error = f.errors['password'][0]
                    print(f"Sorry, something wrong with your password:\n{colorama.Fore.RED}{error}{colorama.Style.RESET_ALL}\nPlease try again.")

        print(f"Creating with your username {colorama.Fore.GREEN}{username}{colorama.Style.RESET_ALL} and {colorama.Fore.GREEN}********{colorama.Style.RESET_ALL}")

        the_user = User.objects.create_user( username, '', password)
        the_user.is_staff = True
        the_user.is_superuser = True
        the_user.role = ROLE_ADMIN
        the_user.save()
        print("User created. You can now sign in.")

SETTINGS_CUSTOMIZED_DEFAULT = '''
############### E-mail Backend https://github.com/django-ses/django-ses ####################

############### E-mail settings with AWS
# EMAIL_BACKEND = "django_ses.SESBackend"
# AWS_SES_REGION_NAME = "us-west-2"
# AWS_SES_REGION_ENDPOINT = "email.us-west-2.amazonaws.com"
# SERVER_EMAIL = ""
# SES_SENDER_EMAIL = ""

#### If you have setup your AWS IAM profile, there is no need to setup the Access Key and Secrets for the Security Group
#AWS_SECURITY_GROUP_KEY_ID = 'YOUR-ACCESS-KEY-ID'
#AWS_SECURITY_GROUP_ACCESS_KEY = 'YOUR-SECRET-ACCESS-KEY'
'''

def check_and_create_settings_customized():
    settings_customized_path = "securitygroups/settings_customized.py"
    if not os.path.exists(settings_customized_path):
        f = open(settings_customized_path, "w")
        f.write(SETTINGS_CUSTOMIZED_DEFAULT)
        f.close()
        print(f"Created a new {colorama.Fore.GREEN}securitygroups/settings_customized.py{colorama.Style.RESET_ALL} file.")


def check_and_create_env():
    if not os.path.exists( ".env"):
        print(f"{colorama.Fore.RED}Your system has not initialized.{colorama.Style.RESET_ALL}")

        # Create a .env file
        print(f"{colorama.Fore.GREEN}Create a .env file with default settings{colorama.Style.RESET_ALL}")
        create_default_file()

        # Schedule migrate thread in 3 seconds
        thread_ = threading.Thread(target=migrate_thread, args=[], kwargs={})
        thread_.start()

# Run migrate
def migrate_thread():
    print(f"The database of the Uptime Checker is not ready yet. One moment...")

    print(f"{colorama.Fore.GREEN}Creating SQLite database in {colorama.Fore.RED}4{colorama.Fore.GREEN} seconds{colorama.Style.RESET_ALL}")
    time.sleep(1)
    print(f"{colorama.Fore.GREEN}Creating SQLite database in {colorama.Fore.RED}3{colorama.Fore.GREEN} seconds{colorama.Style.RESET_ALL}")
    time.sleep(1)
    print(f"{colorama.Fore.GREEN}Creating SQLite database in {colorama.Fore.RED}2{colorama.Fore.GREEN} seconds{colorama.Style.RESET_ALL}")
    time.sleep(1)
    print(f"{colorama.Fore.GREEN}Creating SQLite database in {colorama.Fore.RED}1{colorama.Fore.GREEN} seconds{colorama.Style.RESET_ALL}")
    time.sleep(1)
    print(f"{colorama.Fore.GREEN}Creating...{colorama.Style.RESET_ALL}")

    call_command('migrate', verbosity=0, interactive=True)
    print(
        f"{colorama.Fore.RED}Done! {colorama.Fore.GREEN}Database should be ready to go!{colorama.Style.RESET_ALL}")

    print(
        f"If the database file is not created, just run: {colorama.Fore.RED}python manage.py migrate{colorama.Style.RESET_ALL}\n")

    create_first_user()

def is_docker():
    return os.getenv("IS_DOCKER")

# Only check the first run has no users if it's DEBUG mode
def first_run_has_no_users():
    from django.conf import settings
    if settings.DEBUG:
        if is_docker():
            return True

        try:
            from django.contrib.auth import get_user_model
            from django.conf import settings
            User = get_user_model()

            return (len( User.objects.all() ) == 0)
        except:
            return False
    else:
        False
