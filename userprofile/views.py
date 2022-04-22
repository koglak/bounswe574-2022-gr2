
# Create your views here.
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render
from blog.models import Post
from quiz.models import Case, Question, QuestionList, Score
from .models import Course, Profile, Rating, Lecture
from .forms import CourseForm, ProfileForm, LectureForm
from django.shortcuts import redirect, get_object_or_404
from taggit.models import Tag
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url="/login")
def user_profile(response):
    courses=Course.objects.filter(user = response.user).order_by('published_date')
    user_profile=Profile.objects.get(user=response.user)
    collaborative_member=Course.objects.filter(collaborative_members = response.user)
    question=Post.objects.filter(author=response.user)
    return render(response, "userprofile/profile.html", {'courses':courses, 'user_profile':user_profile, 'collaborative_member': collaborative_member, 'question':question})

@login_required(login_url="/login")
def course_detail(request, title):
    course =Course.objects.get(title=title)
    quiz_list = QuestionList.objects.filter(course=course)
    case_list = Case.objects.filter(course=course)
    score_list = Score.objects.filter(user=request.user)
    context = {
            'course': course,
            'quiz_list':quiz_list,
            'score_list':score_list,
            'case_list':case_list
        }

    return render(request, 'userprofile/course_detail.html', context)


@login_required(login_url="/login")
def course_edit(request, title):
    course = get_object_or_404(Course, title=title)
     
    if request.method == "POST":
        form = CourseForm(request.POST or None, request.FILES or None, instance=course)
        if form.is_valid():
            course = form.save(commit=False)
            course.published_date = timezone.now()
            course.save()
            form.save_m2m()
            return redirect('course_detail', title=course.title)
    else:
        form = CourseForm(instance=course)
    return render(request, 'userprofile/course_edit.html', {'form': form, 'title': title})

@login_required(login_url="/login")
def course_new(request):
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.published_date = timezone.now()
            course.save()
            form.save_m2m()

            return redirect('course_detail', title=course.title)
    else:
        form = CourseForm()
        title ="none"
    return render(request, 'userprofile/course_edit.html', {'form': form, 'title':title})

@login_required(login_url="/login")
def course_tag_detail(response,tag):
    courses = Course.objects.filter(tags__name__in=[tag])
    return render(response, "userprofile/course_tag_details.html", {'courses': courses, 'tag': tag})


def delete_course(request, title):
    course = Course.objects.get(title=title)
    course.delete()
    return redirect('/myspace/profile')


def course_rate(request, title):
    course = get_object_or_404(Course, title=title)
    rating=request.POST["rating"]
    if course.rating_set.filter(user=request.user, rating=rating ):
        print('already rated')
    elif course.rating_set.filter(user=request.user):
        obj= Rating.objects.get(user=request.user, course=course)
        obj.rating = rating
        obj.save()
        course.averagereview()

    else:
        obj = Rating.objects.create(course=course, user=request.user, rating=rating)
        obj.save()
        course.averagereview()

    return redirect('/myspace/profile', title=course.title)


def other_user_profile(response, name):
    courses=Course.objects.filter(user__username=name).order_by('published_date')
    user_profile=Profile.objects.get(user__username=name)
    collaborative_member=Course.objects.filter(collaborative_members__username = name)
    question=Post.objects.filter(author=user_profile.user)

    return render(response, "userprofile/profile.html", {'courses': courses, 'user_profile': user_profile, 'collaborative_member': collaborative_member, 'question': question})

def profile_edit(request,pk):
    profile = get_object_or_404(Profile, pk=pk)

    if request.method == "POST":
        form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            form.save_m2m()
            return redirect('user_profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'userprofile/profile_edit.html', {'form': form})

def lecture_detail(response, pk):
    lecture = get_object_or_404(Lecture, pk=pk)
    course = Course.objects.filter(lecture__title=lecture.title)
    quiz_list = QuestionList.objects.filter(course=course)
    score_list = Score.objects.filter(user=response.user)
    context = {
            'course': course,
            'lecture': lecture,
            'quiz_list':quiz_list,
            'score_list':score_list,
        }

    return render(response, "userprofile/lecture_detail.html",context)


def search_course(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        results = Course.objects.filter(title__icontains=searched)

        return render(request, "userprofile/search_course.html", {'searched': searched, 'results': results}) 
    else:
        return render(request, "userprofile/search_course.html", {}) 

def course_enroll(request,pk):
    course = get_object_or_404(Course, pk=pk)

    course.enrolled_users.add(request.user)
    title=course.title
    
    return redirect('course_detail', title=title)

def course_drop(request,pk):
    course = get_object_or_404(Course, pk=pk)

    course.enrolled_users.remove(request.user)
    title=course.title
    
    return redirect('course_detail', title=title)


def lecture_new(request, pk):
    if request.method == "POST":
        course = Course.objects.get(pk=pk)
        form = LectureForm(request.POST)
        if form.is_valid():
            lecture = form.save(commit=False)
            lecture.user = request.user
            lecture.published_date = timezone.now()
            lecture.course = course
            lecture.save()
            return redirect('lecture_detail', pk=lecture.pk)
    else:
        form = LectureForm()
        title ="none"
    return render(request, 'userprofile/lecture_edit.html', {'form': form, 'title':title})

def lecture_edit(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk)

    if request.method == "POST":
        course= Course.objects.get(lecture__pk=lecture.pk)

        form = LectureForm(instance=lecture, data=request.POST)
        if form.is_valid():
            form.save()

            return redirect('course_detail', title=course.title)
    else:
        form = LectureForm(instance=lecture)

    return render(request, 'userprofile/lecture_edit.html', {'form': form, 'title': lecture.title})


def delete_lecture(request, title):
    lecture = Lecture.objects.get(title=title)
    course= Course.objects.get(lecture__pk=lecture.pk)

    lecture.delete()
    return redirect('course_detail', title=course.title)

@login_required(login_url="/login")
def learn_page(response):
    course = Course.objects.filter(enrolled_users=response.user)
    return render(response, "userprofile/learn.html", {'course': course})
