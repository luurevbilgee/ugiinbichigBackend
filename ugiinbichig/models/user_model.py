from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password  # make_password-ийг импортлох
from django.utils.translation import gettext_lazy as _
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, phone_number, password=None):
        if not email:
            raise ValueError('Танд email заавал шаардлагатай байна.')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phone_number, password=None):
        return self.create_user(username, email, phone_number, password)


class User(AbstractBaseUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=200)
    verify = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        """Нууц үгийг шифрлэх"""
        self.password = make_password(raw_password)
