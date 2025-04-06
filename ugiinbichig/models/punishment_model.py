from django.db import models
from .human_model import Human
class Punishment(models.Model):
    punishment_id = models.BigAutoField(auto_created=True, primary_key= True, serialize=False, verbose_name="ID", unique=True)
    human = models.ForeignKey(Human , on_delete=models.CASCADE)
    punishment_time = models.DateField()
    shaltgaan = models.TextField(null = True, blank=True)
    imprisoned = models.BooleanField(null=True, blank=True)