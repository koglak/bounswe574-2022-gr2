from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


class Activity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    enrolled_users = models.ManyToManyField(User, blank=True, related_name='activity_enrolled_users')
    
    def __str__(self):
        return self.title
