from django import forms

from .models import Post, Answer, Label
from django.forms import  TextInput

from taggit.forms import TagWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'tags')
        widgets = {
            'title': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Title',
                }),
            'text': forms.Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Text',
                }),
            'tags': TagWidget(),}

class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('body',)
        labels = {
        'body': (''),
         }

class LabelForm(forms.ModelForm):

    class Meta:
        model = Label
        fields =('name',)       