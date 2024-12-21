from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class UserProfile(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phonenumber = models.BigIntegerField()
    password = models.CharField(max_length=200)
    password2 = models.CharField(max_length=200)

    def __str__(self):
        return self.username



class LoginTable (models.Model):
    username= models. CharField(max_length=200)
    password=models.CharField(max_length=200)
    password2=models.CharField(max_length=200)
    type=models.CharField(max_length=200)
    def __str__(self):
        return self.username