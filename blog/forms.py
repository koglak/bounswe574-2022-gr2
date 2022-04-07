from django import forms

from .models import Post, Answer, Label

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)

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