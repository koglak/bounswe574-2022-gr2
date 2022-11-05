from django import forms

from .models import Lecture, Profile,Course, Event
from django.forms import ImageField, ModelForm, TextInput
from taggit.forms import TagWidget
from django.utils.safestring import mark_safe
from django.forms.widgets import NumberInput
from tinymce.widgets import TinyMCE



# RATING_CHOICES = [(i+1,i+1) for i in range(5)]

class TinyMCEWidget (TinyMCE) :
    def use_required_attribute(self, *args):
        return False

class CourseForm(forms.ModelForm):
    description = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    
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
    bio = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    class Meta:
        model = Profile
        fields = ('bio', 'img')

class LectureForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = Lecture
        fields = ('title', 'content')


class EventForm(forms.ModelForm):

    description = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    
    class Meta:
        model = Event
        fields = ('title', 'description', 'start_time')

        widgets = {
            'start_time': NumberInput(attrs={'type':'date'}),
        }

   
                
