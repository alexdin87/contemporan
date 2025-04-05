from django.db import models
import os
from django.conf import settings

class Painting(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    year = models.PositiveIntegerField(null=True, blank=True)
    author = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    image = models.ImageField(upload_to='paintings/', blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.image:
            self.image.name = 'paintings/placeholder.jpg'
        super().save(*args, **kwargs)
