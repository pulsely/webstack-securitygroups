from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid, os
from django.utils import timezone
from django.urls import reverse

# Create your models here.
ROLE_ADMIN = "admin"
ROLE_USER = "user"

class User(AbstractUser):
    # The ID is UUID field, for easy reference with DynamoDB
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')

    ROLES_CHOICES = (
        (ROLE_USER, 'User'),
        (ROLE_ADMIN, 'Admin'),
    )

    # Set the default role to job seeker, in case a mistake is made!
    role = models.CharField(max_length=20, choices=ROLES_CHOICES, default=ROLE_USER)

    AUTH_TYPE = (
        ('system', 'System'),
        #('firebase', 'Firebase'),
    )
    auth_type = models.CharField(max_length=20, choices=AUTH_TYPE, default='system')
    flag_email_confirmed = models.BooleanField( default=False, help_text="Only users with e-mail confirmed can submit job application and employer features" )

    def role_is_staff(self):
        return self.is_staff or self.role == ROLE_ADMIN

    def role_is_user(self):
        return self.role == ROLE_USER

    def role_is_admin(self):
        return self.role == ROLE_ADMIN

    class Meta:
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'