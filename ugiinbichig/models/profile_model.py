from django.db import models
from .human_model import Human

class ProfilePicture(models.Model):
    profile = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID", unique=True)
    human = models.OneToOneField(Human, on_delete=models.CASCADE, related_name="profile_picture")
    image = models.ImageField(upload_to='profile_pictures/')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # human загвараас username-г авах
        return f"Profile picture for {self.human.user.username}"
