from django.db import models
from .human_model import Human
class Divorce(models.Model):
    divorce_ID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID" , unique=True)
    human = models.ForeignKey(Human , on_delete= models.CASCADE , related_name="divorces")
    divorced = models.ForeignKey(Human, on_delete= models.CASCADE, related_name="divorced_by")
    divorce_date = models.DateField()
    shaltgaan = models.TextField(null=True, blank= True)
