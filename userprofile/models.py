
# Create your models here.
from email.mime import image
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(default="This is my bio!")
    img = models.ImageField(upload_to='images')
    followers = models.ManyToManyField(User, related_name='followers', blank=True)

    def __str__(self):
        return self.bio

class Course(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description=models.TextField()
    img = models.ImageField(upload_to='images')
    published_date=models.DateTimeField(blank=True, null=True)
    collaborative_members = models.ManyToManyField(User, blank=True, related_name='collaborative_members')
    tags = TaggableManager()

    def __str__(self):
        return self.title

