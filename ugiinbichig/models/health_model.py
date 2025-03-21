from django.db import models
from .human_model import Human

class Health(models.Model):
    health_ID = models.BigAutoField(auto_created = True, primary_key= True, serialize= False, verbose_name = "ID", unique= True)
    human = models.ForeignKey(Human, on_delete=models.CASCADE)
    history = models.TextField(null = True, blank=True)
    health_date = models.DateField()