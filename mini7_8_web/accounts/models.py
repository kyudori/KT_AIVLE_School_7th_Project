from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import jwt
from datetime import datetime, timedelta
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, user_id, password, name, email):
        if not user_id:
            raise ValueError('The User ID must be set')
        user = self.model(user_id=user_id, name=name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password, name, email):
        user = self.create_user(user_id, password=password, name=name, email=email)
        user.is_admin = True
        user.is_staff = True  # Ensure is_staff is set to True for superuser
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    user_id = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Ensure is_staff field is added

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['name', 'email']

    def __str__(self):
        return self.user_id

    @property
    def token(self):
        token = jwt.encode({'user_id': self.user_id, 'exp': datetime.utcnow() + timedelta(hours=24)}, settings.SECRET_KEY, algorithm='HS256')
        return token

    @property
    def is_superuser(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
