
from django.db import models

from users.models import User

from taggit.managers import TaggableManager

class Image(models.Model):

    title = models.CharField(max_length=45)

    description = models.CharField(max_length=250)

    created = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to='photos/')

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    tags = TaggableManager()

    def __str__(self):
        return self.title