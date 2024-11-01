"""Declare models for YOUR_APP app."""

from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from subscription.models import Subscription

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save()
        
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    
    email = models.EmailField(_('email address'), unique=True)
    units = models.CharField(max_length=2, blank=False, default='in')
    weightUnits = models.CharField(max_length=2, blank=False, default='lb')
    dateTimeFormat = models.CharField(max_length=40, blank=False, default='MMM d, yyyy, h:mm aa')
    multiBinPack = models.BooleanField(default=False)
    disableFillContainerAnimation = models.BooleanField(default=False)
    disablePreviousNextItemAnimation = models.BooleanField(default=False)
    animationSpeed = models.IntegerField(default=100)
    usersTermsOfServiceRevision = models.IntegerField(default=0)
    phoneNumber=models.CharField(max_length=100, blank=True, default='')
    addressLine1 = models.CharField(max_length=100, blank=True, default='')
    addressLine2 = models.CharField(max_length=100, blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    stateProvince = models.CharField(max_length=50, blank=True, default='')
    country = models.CharField(max_length=50, blank=True, default='')
    postalCode = models.CharField(max_length=20, blank=True, default='')
    includeUpsContainers = models.BooleanField(default=True)
    includeUspsContainers = models.BooleanField(default=True)
    shippoAccessToken=models.CharField(max_length=100,blank=True,default='')
    def userHasShippoAccount(self):
        if self.shippoAccessToken:
            return True
        else:
            return False
    @property
    def termsOfServiceRevision(self):
        termsOfServiceRevision = 2
        return termsOfServiceRevision

