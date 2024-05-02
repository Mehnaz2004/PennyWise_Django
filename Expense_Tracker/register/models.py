from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30)
    dob = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    phoneno = models.CharField(max_length=15, blank=True, null=True)
    
    
    def delete_account(self):
        self.delete()

