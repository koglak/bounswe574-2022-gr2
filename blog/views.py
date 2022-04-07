import re
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Answer, Post, Label
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, AnswerForm, LabelForm
from django.shortcuts import redirect
from django.urls import reverse,reverse_lazy



# Create your views here.
def question(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/question_list.html', {'posts': posts})

def question_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.post = post
            answer.name = request.user
            answer.save()
            form = AnswerForm()
    else:
        form = AnswerForm()
    return render(request, 'blog/question_detail.html', {'post': post, "form":form})

def question_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        label = LabelForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('question_detail', pk=post.pk)
    else:
        form = PostForm()
        label = LabelForm()
    return render(request, 'blog/question_edit.html', {'form': form, 'label': label})


def question_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('question_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/question_edit.html', {'form': form})



def label_detail(response,name):
    label=Label.objects.filter(name=name)
    return render(response, "blog/label_details.html", {'label': label, 'name': name})




def home(response):
    return render(response, "blog/home.html", {})



def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    post.dislikes.remove(request.user)
    return redirect('question_detail', pk=pk)

def LikeViewList(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    post.dislikes.remove(request.user)
    return redirect('question')

def DislikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.dislikes.add(request.user)
    post.likes.remove(request.user)
    return redirect('question_detail', pk=pk)

def DislikeViewList(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.dislikes.add(request.user)
    post.likes.remove(request.user)
    return redirect('question')


