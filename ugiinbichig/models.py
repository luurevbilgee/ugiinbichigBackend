from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length= 100, unique= True )
    phone_number = models.CharField(max_length=10)
    password = models.CharField(max_length=200, unique = True)