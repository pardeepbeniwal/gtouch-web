from statistics import mode
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models

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
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username