from django.db import models
from .human_model import Human
class Death(models.Model):
    death_ID = models.BigAutoField(auto_created=True, primary_key= True, serialize=False, verbose_name="ID", unique=True)
    human = models.ForeignKey(Human , on_delete=models.CASCADE)
    death_time = models.DateField()
    shaltgaan = models.TextField(null = True, blank=True)