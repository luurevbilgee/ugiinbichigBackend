from django.db import models
from .human_model import Human,User

class Shape (models.Model):
    shape_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID", unique=True)
    x = models.FloatField()
    y = models.FloatField()
    type = models.CharField(max_length=100, blank = True, null=True)
    color = models.CharField(max_length=100, blank = True, null=True)
    parent_id = models.IntegerField(null = True, blank = True)
    label= models.CharField(max_length=120, null = True, blank = True)
    human_ID = models.OneToOneField(
        Human, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        unique=True  # 🎯 Давхардахаас сэргийлэх
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = False, blank = False)
    is_verified = models.BooleanField(default=False)  # Баталгаажсан эсэхийг тэмдэглэх талбар

    def __str__(self):
        return f"Shape {self.shape_id} at ({self.x}, {self.y})"
    