from django.db import models
from django.utils import timezone
#from users.models import User
from django.urls import reverse
from django.conf import settings

# Create your models here.

class Video(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    upload_date = models.DateTimeField(default=timezone.now)
    video = models.FileField(upload_to="videos/")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("video-detail", kwargs={"pk": self.pk})