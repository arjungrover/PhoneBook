import binascii, os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser,  PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings

from base.models import BaseModel

class UserManager(BaseUserManager):
    """
    This is my custom user manager
    """
    def _create_user(self, phone_number, first_name, password, **extra_fields):
        """
        It will create user with entered phone_number and password
        """
        if not phone_number:
            raise ValueError("The given Phone number must be set")
        if not first_name:
            raise ValueError("First Name must be set")
        user = self.model(phone_number=phone_number, first_name=first_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_user(self, phone_number, first_name, password, **extra_fields):
        extra_fields['is_superuser'] = False
        extra_fields['is_staff'] = True
        return self._create_user(phone_number, first_name, password, **extra_fields)

    def create_superuser(self, phone_number, first_name, password, **extra_fields):
        extra_fields['is_superuser'] = True
        extra_fields['is_staff'] = True
        return self._create_user(phone_number, first_name, password, **extra_fields)
         

class UserInfo(BaseModel, AbstractBaseUser, PermissionsMixin):
    """
    This model will store all information related to users
    """
    phone_number = models.CharField(verbose_name="Phone number", max_length=15, unique=True)
    email = models.EmailField(verbose_name="Email Id", max_length=255, blank=True)
    first_name = models.CharField(verbose_name="First Name", max_length=50)
    last_name = models.CharField(verbose_name="Last Name", max_length=50, blank=True)
    password = models.CharField(verbose_name="Password", max_length=128)
    is_verified = models.BooleanField(default=False, help_text="Designates whether the phone number is verified")
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, help_text="Designates whether the user can log into this admin site.")

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

    def __str__(self):
        return "{}:{}".format(self.first_name,self.phone_number)

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

class Token(BaseModel, models.Model):
    """
    This model will store token which will be used to authenticate users
    """
    key = models.CharField(verbose_name="Token Key", unique=True, max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_valid = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()

        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()
    
    def __str__(self):
        return self.key
