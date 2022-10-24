from django import forms

from .models import Lecture, Profile,Course, Event
from django.forms import ImageField, ModelForm, TextInput
from taggit.forms import TagWidget
from django.utils.safestring import mark_safe
from django.forms.widgets import NumberInput



# RATING_CHOICES = [(i+1,i+1) for i in range(5)]


class CourseForm(forms.ModelForm):
    class Meta:
       model = Course
       fields = ('title', 'description','img', 'collaborative_members', 'tags')
       widgets = {
            'title': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Name',
                }),
            'description': forms.Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Name',
                }),
            'tags': TagWidget(),
            'img': forms.FileInput(),
                }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'img')

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ('title', 'content')


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('title', 'description', 'img', 'event_date', 'event_time', 'category', 'link')

        widgets = {
            'event_date': NumberInput(attrs={'type':'date'}),
            'event_time': forms.TimeInput(attrs={'type': 'time'}),
            'img': forms.FileInput(),
        }

   
                
