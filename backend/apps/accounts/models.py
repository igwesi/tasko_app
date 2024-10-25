from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
LEVELS = [
    (1, 'Beginner'), 
    (2, 'Intermediate'), 
    (3, 'Advanced'), 
    (4, 'Expert'),
    (5, 'Super Expert'), 
    (6, 'Master'), 
    (7, 'Grand Master'), 
    (8, 'Legend'), 
]

class Account(AbstractBaseUser, PermissionsMixin):
    email       = models.EmailField(verbose_name="email", max_length=60, unique=True)
    level       = models.CharField(max_length=200, choices=LEVELS, default=1)

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login  = models.DateTimeField(verbose_name='last login', auto_now=True)

    is_admin    = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
        
    def level_upgrade(self):
        """
        Automatically upgrade the user's level after a specific period of days of registration.
        This method checks if the user has been registered for more than 7 days.
        If yes, it upgrades the user's level by 1.
        """
        from datetime import datetime, timedelta
        if self.date_joined + timedelta(days=7) < datetime.now():
            self.level = 2
        elif self.datetime_joined + timedelta(days=14) < datetime.now():
            self.level = 3
        elif self.datetime_joined + timedelta(days=21) < datetime.now():
            self.level = 4
        elif self.datetime_joined + timedelta(days=28) < datetime.now():
            self.level = 5
        elif self.datetime_joined + timedelta(days=35) < datetime.now():
            self.level = 6
        elif self.datetime_joined + timedelta(days=42) < datetime.now():
            self.level = 7
        elif self.datetime_joined + timedelta(days=49) < datetime.now():
            self.level = 8
        self.save()

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Users'