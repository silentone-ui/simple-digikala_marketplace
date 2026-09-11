from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings


class UserManager(BaseUserManager):
    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError('شماره موبایل باید وارد شود')

        first_name = extra_fields.get('first_name')
        last_name = extra_fields.get('last_name')

        if not first_name or not last_name:
            raise ValueError('نام و نام خانوادگی باید وارد شود')

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(phone_number, password or '', **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser باید is_staff=True باشد')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser باید is_superuser=True باشد')

        return self._create_user(phone_number, password or '', **extra_fields)


class User(AbstractUser):
    username = None
    first_name = models.CharField('اسم', max_length=50)
    last_name = models.CharField('فامیل', max_length=50)
    phone_number = models.CharField(max_length=11, unique=True)
    is_seller = models.BooleanField(default=False)
    balance = models.PositiveIntegerField(default=0)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=300)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.full_name