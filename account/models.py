from statistics import mode
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email,  password=None, is_admin=False, is_staff=False, is_active=True):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        #user.full_name = full_name
        user.set_password(password)  # change password to hash
        #user.profile_picture = profile_picture
        user.admin = is_admin
        user.staff = is_staff
        user.active = is_active
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")


        user = self.model(
            email=self.normalize_email(email)
        )
        #user.full_name = full_name
        user.set_password(password)
        #user.profile_picture = profile_picture
        user.admin = True
        user.staff = True
        user.active = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    email = models.EmailField(verbose_name='email address', max_length=255, blank=True, null=True)
    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = []
    mobile_number = models.BigIntegerField(max_length=12, unique=True)
    passcode = models.CharField(blank=True, null=True,max_length=10)
    status = models.IntegerField(default=0)
    device = models.CharField(blank=True, null=True,max_length=255)
    device_id = models.CharField(blank=True, null=True,max_length=255)

    objects = UserManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username



   