from datetime import timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render

from quiz.models import Case, QuestionList
import userprofile
from .models import Answer, Post, Profile
from userprofile.models import Course
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, AnswerForm
from django.shortcuts import redirect
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# Create your views here.


@login_required(login_url="/login")
def question(request):
    common_tags = Post.tags.most_common()[:4]
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/question_list.html', {'posts': posts, 'common_tags': common_tags})


@login_required(login_url="/login")
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


@login_required(login_url="/login")
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



@login_required(login_url="/login")
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



@login_required(login_url="/login")
def question_tag_detail(response,tag):
    posts = Post.objects.filter(tags__name__in=[tag])
    return render(response, "blog/question_tag_details.html", {'posts': posts, 'tag': tag})

def home(response):
    courses = Course.objects.all()
    enrolled_courses = Course.objects.all()
    ids = (course.id for course in enrolled_courses)
    quizes = QuestionList.objects.filter(course__in=ids)    
    cases = Case.objects.all()[:5]

    if response.user.is_authenticated:
        courses = Course.objects.filter(enrolled_users=response.user)[:5]
        enrolled_courses = Course.objects.filter(enrolled_users=response.user)
        ids = (course.id for course in enrolled_courses)
        quizes = QuestionList.objects.filter(course__in=ids)    
        cases = Case.objects.all()[:5]

    common_tags = Course.tags.most_common()[:5]
    num_of_courses = len(Course.objects.filter(timestamp=timezone.now() - timedelta(days=7)))
    num_of_users = len(Profile.objects.filter(timestamp=timezone.now() - timedelta(days=7)))

    paginator = Paginator(courses,4) 
    page = response.GET.get('page')
    courses= paginator.get_page(page)


    return render(response, "blog/home.html", {'courses': courses, 'common_tags': common_tags,'num_of_courses':num_of_courses, 'num_of_users':num_of_users, 'quizes':quizes, 'cases':cases})


@login_required(login_url="/login")
def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    post.dislikes.remove(request.user)
    return redirect('question_detail', pk=pk)


@login_required(login_url="/login")
def LikeViewList(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    post.dislikes.remove(request.user)
    return redirect('question')


@login_required(login_url="/login")
def DislikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.dislikes.add(request.user)
    post.likes.remove(request.user)
    return redirect('question_detail', pk=pk)


@login_required(login_url="/login")
def DislikeViewList(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.dislikes.add(request.user)
    post.likes.remove(request.user)
    return redirect('question')


@login_required(login_url="/login")
def delete_question(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('/question')

@login_required(login_url="/login")
def AnswerLikeView(request, pk):
    answer = get_object_or_404(Answer, id=request.POST.get('answer_id'))
    answer.likes.add(request.user)
    answer.dislikes.remove(request.user)
    return redirect('question_detail', pk=pk)


@login_required(login_url="/login")
def AnswerDislikeView(request,pk ):
    answer = get_object_or_404(Answer, id=request.POST.get('answer_id'))
    answer.dislikes.add(request.user)
    answer.likes.remove(request.user)
    return redirect('question_detail', pk=pk)

@login_required(login_url="/login")
def search_question(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        results = Post.objects.filter(title__contains=searched)

        return render(request, "blog/search_question.html", {'searched': searched, 'results': results}) 
    else:
        return render(request, "blog/search_question.html", {}) 
