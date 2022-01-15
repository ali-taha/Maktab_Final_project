from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator




class CustomUser(AbstractUser):
    phone_regex = RegexValidator(regex=r'^0?9\d{9}$', message="Phone number must be entered in the format: '0+'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length=15,unique=True)
    is_seller = models.BooleanField(default=False,help_text=(
            'Does the user have a Shop?'))
    is_phone_active = models.BooleanField(default=False,help_text=('is user phone_number activated?'))
    user_avatar = models.ImageField(upload_to='uploads/user_avatar', blank=True, null=True)    

    REQUIRED_FIELDS = ['email', 'phone_number']


    def __str__(self):
        return self.username