from django.db import models
from .human_model import Human
class Video(models.Model):
    video_ID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID", unique=True)
    human = models.ForeignKey(Human, on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
