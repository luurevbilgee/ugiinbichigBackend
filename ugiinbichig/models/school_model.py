from django.db import models
from .human_model import Human
class School (models.Model):
    school_ID = models.BigAutoField(auto_created = True, primary_key= True, serialize= False, verbose_name= "ID", unique = True)
    human = models.ForeignKey(Human, on_delete=models.CASCADE)
    start_time = models.DateField()
    end_time = models.DateField()
    school_name = models.CharField(max_length=250)
    zereg = models.CharField(max_length=250, null=True, blank=True)