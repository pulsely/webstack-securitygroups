
# Security Groups Webstack by Pulsely

__Security Groups Webstack__ is a Django powered webstack solution developed by [Pulsely](https://www.pulsely.com/). 
__Security Groups Webstack__ let you control the access of a specific Security Group in an Amazon Web Services Virtual Private Network.

---

## Running the Security Groups Webstack

You can run the Security Groups Webstack directly with a Python virtual environment, or with Docker.

### Running with Python Virtual Environment

The best way would be to create a new Python virtual environment. Any Python with version 3.9 should work.
The only dependency would be an active Redis 4.0+ installation.

* Pull the source code of Job Hunting Webstack:
  ```sh
  git clone https://github.com/pulsely/webstack-securitygroups
  ```

* Changed to the directory of the Job Hunting Webstack:
  ```sh
  cd webstack-securitygroups
  ```

* Create a new python virtual environment and install the packages from requirements.txt:
  ```sh
  python -m venv venv
  source ./venv/bin/activate
  pip install -r requirements.txt
  ```
(Your Python 3 runtime could be named differently, such as 'python3', so change to ```python3 -m venv venv``` if this is the case.)

* Then run the Security Groups Webstack:
  ```sh
  python manage.py runserver
  ```
  The manage.py will check if a .env file is create and create one for you automatically if missing. The db.sqlite3 file will also be created for you 4 seconds after the installation is fired up the first time.
* You can run your Security Groups Webstack in development mode with the Make command ```make dev```, or activate the venv virtual environment created previously with these commands:
  ```sh
  source ./venv/bin/activate
  python manage.py runserver
  ```


### Running with Docker

The Security Groups Webstack has a default DockerFile which will run with Docker or Podman in development mode.

* The Docker setup will run the Security Groups Webstack with Django, and run the first run setup automatically.

  ```sh
  docker-compose up
  ```

* To run the Docker setup in daemon mode:

  ```sh
  docker-compose up -d
  docker-compose run django python manage.py createsuperuser
  ```

[//]: # (---)

[//]: # ()
[//]: # (###  Celery)

[//]: # ()
[//]: # (Celery is used for scheduling the periodic uptime checks.)

[//]: # ()
[//]: # (A sample shell script will trigger the celery for recurring checks with minutes specified in ``DEFAULT_PERIODIC_MINUTES`` with the .env configuration:  )

[//]: # (```./run_celery_dev.sh``` )

---

### Django settings that can be overwritten

These settings are stored at the ``.env`` file and can be overwriten at the default Django settings at ```securitygroups/settings_customized.py``` which should be created on first run.

| **Varaiable** | **Description**                                                  | **Defaults**                           |
| ------------- |------------------------------------------------------------------|----------------------------------------|
| ``SECRET_KEY`` | The secret key for Django user authentication                    | ``Random key generated automatically`` |
| ``DEBUG``          | Django DEBUG mode for development. Set to false for deployment   | ``true``                               |
| ``ALLOWED_HOSTS``   | Host/domain names that this Django site can serve.               | ``*``                                  |
| ``AWS_REGION_SECURITY_GROUP`` | **AWS Region of the Security Group**                             | ``ap-northeast-1``                     |
| ``AWS_EC2_SECURITY_GROUP`` | **The Security Group ID**                                        | ``sg-xxxxxxxxxx``                      |
| ``EMAIL_BACKEND`` | The default E-mail backend, set to django-ses for AWS deployment | ``django_ses.SESBackend``              |
| ``AWS_SES_REGION_NAME`` | Default AWS SES region Name                                      | ``us-west-2``                          |
| ``AWS_SES_REGION_ENDPOINT`` | Default AWS SES region endpoint                                  | ``email.us-west-2.amazonaws.com``      |
| ``SERVER_EMAIL`` | E-mail for sending the notification emails                       |                                        |

[//]: # (| ``SLACK_TOKEN`` | Slack Team Token                                                            |                                                                                      |)

[//]: # (| ``SLACK_ROOM`` | Room to show the error Slack message.                                       | ``#general``                                                                                                           |)

### Optional Access Key and Secret settings that can be added

These settings can be overwriten at the default Django settings at ```securitygroups/settings_customized.py``` which should be created on first run.

| **Varaiable** | **Description**                                                   | **Defaults** |
| ------------- |-------------------------------------------------------------------|--------------|
| ``AWS_SECURITY_GROUP_KEY_ID`` | **Access ID** of IAM user which has access to the Security Group  |   ``-``           |
| ``AWS_SECURITY_GROUP_ACCESS_KEY``          | **Access Key** of IAM user which has access to the Security Group | ``-``        |


---
## Special notes on deployment

If you deploy to production such as Nginx with Supervisord, you will need to overwrite the default ``CSRF_TRUSTED_ORIGINS`` variable at the file ``securitygroups/settings_customized.py``.

Configuration details of the ``CSRF_TRUSTED_ORIGINS`` is available at [Django website](https://docs.djangoproject.com/en/4.2/ref/settings/#csrf-trusted-origins)

---

## Django Management Commands



Type ```python manage.py``` to check for the default Django management commands available:

```
migrate
createsuperuser
changepassword
```

```python manage.py migrate``` will create database schema on your database settings. It should automatically run by manage.py the first time though.

```python manage.py createsuperuser``` allows you to create superuser at the command line.

```python manage.py changepassword``` let you change password for any user in the system.

These Job Hunting Webstack commands are available for testing and house cleaning.
```
mail_test
reset
```

```python manage.py mail_test``` can be used for sending test e-mail(s) to check your notification configurations.

```python manage.py reset``` will remove the .env, db.sqlite3, celerybeat-schedule and jobhunting/settings_customized.py configuration files to reset your installation.   
**(Only available for DEBUG mode on.)**

---

## Running databases other than SQLite?

You can use any databases supported by Django. Create the database settings at the jobhunting/settings.py file following the Django documentations, and you should be good to go.

---

# Credits & Acknowledgements

This project utilizes the following components:

### Python packages

[//]: # (* __Celery__  )

[//]: # (  Copyright &#40;c&#41; 2015-2016 Ask Solem & contributors.  All rights reserved.)

[//]: # (  Copyright &#40;c&#41; 2012-2014 GoPivotal, Inc.  All rights reserved.)

[//]: # (  Copyright &#40;c&#41; 2009, 2010, 2011, 2012 Ask Solem, and individual contributors.  All rights reserved.)

[//]: # (  BSD 3-Clause "New" or "Revised" License)

[//]: # (  https://github.com/celery/celery)

* __Django__  
  Copyright (c) Django Software Foundation and individual contributors.   
  All rights reserved.   
  https://www.djangoproject.com/  

* __Django SES__
  Copyright (c) 2011 Harry Marr  
  MIT license  
  https://github.com/django-ses/django-ses  

* __Font Awesome__  
  CC BY 4.0 License
  https://github.com/FortAwesome/Font-Awesome

* __python-decouple__  
  Copyright (c) 2013 Henrique Bastos
  MIT license  
  https://github.com/HBNetwork/python-decouple

### Graphics

* __Admin panel template is provided by CoreUI__  
  Copyright 2022 creativeLabs Łukasz Holeczek. Code released under the MIT License   
  https://github.com/coreui/coreui


---

# Copyright and license

The Security Groups Webstack is written by Pulsely https://www.pulsely.com/

Copyright 2023 Pulsely