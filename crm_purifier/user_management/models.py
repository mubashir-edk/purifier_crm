from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import password_validation


class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, username, password=None, **extra_fields):
        if not email and not username:
            raise ValueError('The Email and Username field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_employee(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_employee', True)
        return self.create_user(email, username, password, **extra_fields)

    def create_customer(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_customer', True)
        return self.create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)
    
    def get_by_natural_key(self, username, **extra_fields):
        return self.get(username=username)
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, validators=[password_validation.validate_password])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True,
    )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True,
    )
    
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser