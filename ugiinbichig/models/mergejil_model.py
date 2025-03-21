from django.db import models
from .human_model import Human
class Mergejil(models.Model):
    mergejil_ID = models.BigAutoField(auto_created= True, primary_key = True, serialize= False, verbose_name = "ID", unique=True)
    human = models.ForeignKey(Human , on_delete=models.CASCADE)
    mergejil = models.CharField(max_length= 250)
