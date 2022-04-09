import re
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Answer, Post
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, AnswerForm
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

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()

            return redirect('question_detail', pk=post.pk)
    else:
        form = PostForm()
        pk ="none"
    return render(request, 'blog/question_edit.html', {'form': form,'pk': pk})


def question_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()

            return redirect('question_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/question_edit.html', {'form': form, 'pk': pk})


def question_tag_detail(response,tag):
    posts = Post.objects.filter(tags__name__in=[tag])
    return render(response, "blog/question_tag_details.html", {'posts': posts, 'tag': tag})


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

def delete_question(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('/question')

def search_question(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        results = Post.objects.filter(title__contains=searched)

        return render(request, "blog/search_question.html", {'searched': searched, 'results': results}) 
    else:
        return render(request, "blog/search_question.html", {}) 
