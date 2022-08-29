from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, User
)
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, phone, password=None, password2=None):
        if not first_name or not last_name or not phone or not email:
            raise ValueError('please fill in all fields!!')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, phone, password=None, password2=None):
    
        user = self.create_user(
            username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
            phone=phone,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    username = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, blank=False, unique=True,
        error_messages={'required': 'Please provide your email address.',
                        'unique': 'An account with this email exist.'},)
    phone = models.CharField(max_length=11, unique=True, 
                            validators=[RegexValidator(regex=r'09(\d{9})$')])
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone', ]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
