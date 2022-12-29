from django import forms
from django.db import models
from django.conf import settings
from userprofile.models import Course
from django.template.defaulttags import register
from django.contrib.auth.models import User
from django.db.models import Avg
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.utils import timezone



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
    timestamp = models.DateTimeField(auto_now_add=True,blank=True, null=True)


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
    published_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(blank = True, null = True)
    

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date']

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text=models.TextField()
    post = models.ForeignKey(Case, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    published_date=models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='comment_like')
    dislikes = models.ManyToManyField(User, related_name='comment_dislike')

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        like=self.likes.count()
        like=like-1
        return self.dislikes.count()

    # when we call __str__, it will turn a text
    def __str__(self):
        return self.text

class ReplyComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="reply_comment")
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='reply_comment_like')
    dislikes = models.ManyToManyField(User, related_name='reply_comment_dislike')

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        like=self.likes.count()
        like=like-1
        return self.dislikes.count()


#    def __str__(self):
#        return '%s - %s' % (self.comment.text, self.body)

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

