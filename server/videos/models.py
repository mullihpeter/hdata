from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Video(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=500)
    upload_date = models.DateTimeField(default=timezone.now())
    video = models.FileField(upload_to="")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("video-detail", kwargs={"pk": self.pk})