from django.db import models
from .user_model import User
class Human (models.Model):
    human_ID  = models.BigAutoField(auto_created= True, primary_key= True, serialize= False, verbose_name="ID")
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    urgiin_ovog = models.CharField(max_length= 150 )
    ovog = models.CharField(max_length= 150)
    ys_undes = models.CharField(max_length= 150)
    name = models.CharField(max_length= 150)
    RD = models.CharField(max_length= 100, verbose_name = "Регистерийн дугаар", unique=True)
    birth_date = models.DateField()
    birth_counter = models.CharField(max_length= 100)
    birth_year = models .CharField(max_length= 100)
    gender = models.CharField(max_length= 100, choices=[
        ('эрэгтэй', 'Эрэгтэй'),
        ('эмэгтэй', 'Эмэгтэй'),
        ('бусад', 'Бусад')
    ])
    
    def __str__(self):
        return f"{self.name} ({self.RD})"
