from django.db import models
from .human_model import Human
class Image(models.Model):
    img_ID = models.BigAutoField(auto_created= True, primary_key= True, serialize=False,verbose_name="ID", unique=True)
    human = models.ForeignKey(Human , on_delete= models.CASCADE)
    image = models.ImageField(upload_to='image/', null=True, blank=True)
    discription = models.CharField(max_length= 250, null = True, blank=True)
    def __str__(self):
        return self.discription
