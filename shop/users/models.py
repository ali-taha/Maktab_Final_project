from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser(AbstractUser):

    phone_number = models.CharField(max_length=15,unique=True)
    is_seller = models.BooleanField(default=False,help_text=(
            'Does the user have a Shop?'
        ))

    REQUIRED_FIELDS = ['email', 'phone_number']


    def __str__(self):
        return self.username