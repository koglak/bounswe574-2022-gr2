from django import forms

from .models import Profile,Course
from django.forms import ImageField, ModelForm, TextInput
from taggit.forms import TagWidget
from django.utils.safestring import mark_safe



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


                
   
                
