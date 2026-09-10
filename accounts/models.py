from django.db import models
from django.contrib.auth.models import AbstractUser , BaseUserManager

class UserManager(BaseUserManager):
    def _create_user(self,phone_number,password,**extra_fields):
        if  not phone_number:
            raise ValueError('phone number must be set')

        user = self.model(phone_number=phone_number,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self,phone_number,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('super user must have is staff True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must have is_superuser True')
        return self._create_user(phone_number,password,**extra_fields)

    def create_user(self,phone_number,password,**extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)
        extra_fields.setdefault('is_active',True)
        return self._create_user(phone_number,password,**extra_fields)


class User(AbstractUser):
    username=None

    phone_number = models.CharField(max_length=11,unique=True)
    is_seller = models.BooleanField(default=False)
    balance = models.PositiveIntegerField(default=0)


    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()
