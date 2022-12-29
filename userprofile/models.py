
# Create your models here.
import datetime
from email.mime import image
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.db.models import Avg
from tinymce import models as tinymce_models

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #bio = models.TextField(default="This is my bio!")
    bio = tinymce_models.HTMLField()
    img = models.ImageField(upload_to='images')
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def __str__(self):
        return self.bio

    def last_7_days_users(self):
        return Profile.objects.filter(date_joined__gte=timezone.now()-datetime.timedelta(days=7)).count()

class Course(models.Model):
   
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    #description=models.TextField()
    description = tinymce_models.HTMLField()
    img = models.ImageField(upload_to='images')
    published_date=models.DateTimeField(blank=True, null=True)
    collaborative_members = models.ManyToManyField(User, blank=True, related_name='collaborative_members')
    enrolled_users = models.ManyToManyField(User, blank=True, related_name='enrolled_users')
    tags = TaggableManager()
    timestamp = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def averagereview(self):
        rating = Rating.objects.filter(course=self).aggregate(avarage=Avg('rating'))
        avg=0
        if rating["avarage"] is not None:
            avg=float(rating["avarage"])
        return avg

    def userProfileImg(self):
        user = Profile.objects.get(user=self.user)
        return user.img

    def __str__(self):
        return self.title

    #write a model which returns the number of Courses created in the last 7 days
    def last_7_days(self):
        return Course.objects.filter(timestamp__gte=timezone.now()-datetime.timedelta(days=7)).count()

    #write a model which returns the number of Users created in the last 7 days
    


class Rating(models.Model):

    course=models.ForeignKey(Course,default=None, on_delete=models.CASCADE)
    user=models.ForeignKey(User,default=None, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.course.title

class Lecture(models.Model):
    course=models.ForeignKey(Course,default=None, on_delete=models.CASCADE, related_name="lecture")
    user=models.ForeignKey(User,default=None, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    #content=models.TextField()
    content = tinymce_models.HTMLField()
    published_date=models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.course.title
class Event(models.Model):
    CATEGORY_CHOICES = (
    ("All", "All"),
    ("Outside", "Outside"),
    ("Workshop", "Workshop"),
    ("Social", "Social"),
    ("Presentation", "Presentation"),
    ("Introductory", "Introductory"),
    ("Training", "Training")
    )

    title = models.CharField(max_length=200)
    #description = models.TextField()
    description = tinymce_models.HTMLField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event_date = models.DateTimeField(default=timezone.now)  
    event_time = models.TimeField(default='20:00')
    enrolled_users = models.ManyToManyField(User, blank=True, related_name='event_enrolled_users')
    course=models.ForeignKey(Course, default=None, on_delete=models.CASCADE, related_name='event_list')
    category = models.CharField(max_length=12,
                  choices=CATEGORY_CHOICES,
                  default="Workshop")
    link= models.URLField(default='http://www.helloworld.com')
    img = models.ImageField(upload_to='images', help_text="event_image", null=True)
    quota = models.PositiveIntegerField(default=0, blank=True)
    published_date = models.DateTimeField(blank=True, null=True, default=timezone.now)  
    duration = models.PositiveIntegerField( default=0, blank=True)


    def get_remaining_days(self):
        return (self.event_date - datetime.datetime.today()).days

    def get_remaining_quota(self):
        if self.quota != 0:
            remaining = (self.quota - self.enrolled_users.count())
        else:
            remaining = 5
        return remaining
    
    def publish_date_check(self):
        return (datetime.datetime.today() - self.published_date).days < 1
         
    
    def __str__(self):
        return self.title


