from django.db import models
from .human_model import Human
class Marry(models.Model):
    marry_ID = models.BigAutoField(auto_created=True, primary_key=True, serialize= False, verbose_name = "ID", unique= True)
    human = models.ForeignKey(Human , on_delete=models.CASCADE, related_name="marries")
    marryd = models.ForeignKey(Human , on_delete=models.CASCADE, related_name="married_to")
    marry_date = models.DateField()