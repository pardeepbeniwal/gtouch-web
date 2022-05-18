from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass
    # add additional fields in here
    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.username