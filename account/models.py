from email.policy import default
from statistics import mode
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
from django.utils import timezone
import uuid



class TimestampMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

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
        
    def create_superuser(self, email='admin@gtouch.com', password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")


        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        #user.profile_picture = profile_picture
        user.admin = True
        user.staff = True
        user.active = True
        user.mobile_number = 1234567890
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    email = models.EmailField(verbose_name='email address', max_length=255, blank=True, null=True)
    #USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    mobile_number = models.BigIntegerField(max_length=12, unique=True)
    passcode = models.CharField(blank=True, null=True,max_length=10)
    status = models.IntegerField(default=0)
    device = models.CharField(blank=True, null=True,max_length=255)
    device_id = models.CharField(blank=True, null=True,max_length=255)
    first_name = models.CharField(blank=True, null=True,max_length=255)
    last_name = models.CharField(blank=True, null=True,max_length=255)
    dob = models.DateField(blank=True, null=True,max_length=255)
    gender = models.CharField(blank=True, null=True,max_length=255)#M=MALE,F=FEMALE
    opt_created_at = models.DateTimeField(default=timezone.now())

    objects = UserManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username

class UserSession(TimestampMixin):
    device_id = models.CharField(blank=True, null=True,max_length=255)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False)
    device_name = models.CharField(blank=True, null=True,max_length=255)
    status = models.IntegerField(default=0)#user is active or not
    access_token = models.TextField(db_index=True,unique=True, default=1)