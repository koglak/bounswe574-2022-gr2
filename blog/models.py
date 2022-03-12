from django.db import models

# Create your models here.

from django.conf import settings
from django.utils import timezone


# Class is special keyword to define object
# Post is name of our model - start uppercase
# models.Model defines it as Django model and save to db
class Post(models.Model):
   
    # link to another model
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # type is char
    title = models.CharField(max_length=200)
    
    #type is text
    text=models.TextField()

    # type is date and time
    created_date = models.DateTimeField(default=timezone.now)
    published_date=models.DateTimeField(blank=True, null=True)


    # use lowercase for methods' name
    def publish(self):
        self.published_date=timezone.now()
        self.save()

    # when we call __str__, it will turn a text
    def __str__(self):
        return self.title


