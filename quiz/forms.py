from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
 
 
class QuestionForm(ModelForm):
    class Meta:
        model=Question
        fields="__all__"