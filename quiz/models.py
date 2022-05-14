from django import forms
from django.db import models
from django.conf import settings
from userprofile.models import Course
from django.template.defaulttags import register
from django.contrib.auth.models import User
from django.db.models import Avg
from django.core.validators import MaxValueValidator, MinValueValidator 


OPTION_CHOICES = (
    ('option1','option1'),
    ('option2', 'option2'),
    ('option3','option3'),
    ('option4','option4'),
)

 
# Create your models here.
class Question(models.Model):
    question = models.CharField(max_length=200,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200, choices=OPTION_CHOICES, default='option1')
    
    def __str__(self):
        return self.question


class QuestionList(models.Model):
    title=models.CharField(max_length=200,null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course=models.ForeignKey(Course, default=None, on_delete=models.CASCADE, related_name='question_list')
    question_list = models.ManyToManyField(Question, blank=True)


    def __str__(self):
        return f'{self.title} {self.course.title}'


class Score(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.CharField(max_length=200,null=True)
    quiz =models.ForeignKey(QuestionList, default=None, on_delete=models.CASCADE)

    @register.filter
    def get_all_scores(self,quiz):
        return self.filter(quiz=quiz).last()

    def __str__(self):
        return self.score

class Case(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course=models.ForeignKey(Course, default=None, on_delete=models.CASCADE, related_name='case_list')
    title=models.CharField(max_length=200,null=True)
    description=models.TextField()

    def __str__(self):
        return self.title

class CaseResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    case=models.ForeignKey(Case, default=None, on_delete=models.CASCADE)
    upload = models.FileField(upload_to='uploads/')
    shared_date=models.DateTimeField(blank=True, null=True)
    
    score=models.IntegerField(null=True, default='0', validators=[MinValueValidator(0), MaxValueValidator(100)])

    def averagereview(self):
        rating = CaseRating.objects.filter(case_result=self).aggregate(avarage=Avg('rating'))
        avg=0
        if rating["avarage"] is not None:
            avg=float(rating["avarage"])
        return avg

    def __str__(self):
        return str(self.score)

class CaseRating(models.Model):

    case_result=models.ForeignKey(CaseResult,default=None, on_delete=models.CASCADE)
    user=models.ForeignKey(User,default=None, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return str(self.rating)

