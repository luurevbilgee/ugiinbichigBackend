from django.db import models
from .human_model import Human
class Who (models.Model):
    who_ID = models.BigAutoField(auto_created= True, primary_key= True, serialize= False, verbose_name= "ID", unique = True)
    human = models.ForeignKey(Human, on_delete = models.CASCADE , related_name="relations")
    relations  = models.ForeignKey(Human , on_delete= models.CASCADE ,related_name= "related_to")
    lavlah = models.CharField(max_length=250)
