# users/models.py
from __future__ import unicode_literals
from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.core.exceptions import ValidationError
from mutual import constant


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password=password, **extra_fields)


class VerifiedUserManager(models.Manager):
    """
    Custom manager for keeping track of people verified till now
    """
    def get_queryset(self):
        return super(VerifiedUserManager, self).get_queryset().filter(verified=True)


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    """
    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=4, blank=True)

    objects = UserManager()
    VerifiedUser = VerifiedUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        self.clean()
        return self

    def get_short_name(self):
        return self.first_name

    def clean(self):
        """
        Any validation of function trigger can be user here
        :return:
        """
        email = self.email
        return email


class Job(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, related_name='user_job')
    company_name = models.CharField(max_length=127, blank=True, null=True)
    company_type = models.CharField(choices=constant.COMPANY_TYPE, max_length=127, blank=True, null=True)
    designation = models.CharField(max_length=50, blank=True, null=True)
    resume = models.FileField(null=True, blank=True)
    # activey_looking = models.BooleanField(default=True)
    # required_designation = models.CharField(choices=constant.REQUIRED_DESIGNATION, max_length=50, blank=True, null=True)

    REQUIRED_FIELDS = ['company_name', 'company_type', 'designation']

    class Meta:
        """
        Define database table name for model, verbose_name, verbose_name_plural
        """
        verbose_name = 'Job'
        verbose_name_plural = 'Users Job'
        db_table = 'Job'

#
# class Employer(models.Model):
#     company_name = models.CharField(max_length=127, blank=True, null=True)
#     company_type = models.CharField(choices=constant.COMPANY_TYPE, max_length=127, blank=True, null=True)
#     vacant_positions = models.CharField(max_length=256, blank=True, null=True)
#
#     class Meta:
#         """
#         Define database table name for model, verbose_name, verbose_name_plural
#         """
#         verbose_name = 'Employer'
#         verbose_name_plural = 'Employer'
#         db_table = 'Employer'
