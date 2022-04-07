
# Create your models here.
from email.mime import image
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField()
    img = models.ImageField(upload_to='images')
    followers = models.ManyToManyField(User, related_name='followers')

    def __str__(self):
        return self.bio

class Course(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description=models.TextField()
    img = models.ImageField(upload_to='images')
    published_date=models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return self.title


class Label(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_labels")
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name