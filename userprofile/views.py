
# Create your views here.
from django.utils import timezone
from django.shortcuts import render
from .models import Course, Profile
from .forms import CourseForm
from django.shortcuts import redirect, get_object_or_404
from taggit.models import Tag
from django.template.defaultfilters import slugify

# Create your views here.

def user_profile(response):
    courses=Course.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    user_profile=Profile.objects.get(user=response.user)
    return render(response, "userprofile/profile.html", {'courses':courses, 'user_profile':user_profile})

def course_detail(request, title):
    course = get_object_or_404(Course, title=title)
    return render(request, 'userprofile/course_detail.html', {'course':course})

def course_edit(request, title):
    course = get_object_or_404(Course, title=title)
     
    if request.method == "POST":
        form = CourseForm(request.POST or None, request.FILES or None, instance=course)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.published_date = timezone.now()
            course.save()
            form.save_m2m()
            return redirect('course_detail', title=course.title)
    else:
        form = CourseForm(instance=course)
    return render(request, 'userprofile/course_edit.html', {'form': form})

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
    return render(request, 'userprofile/course_edit.html', {'form': form})


def course_tag_detail(response,tag):
    courses = Course.objects.filter(tags__name__in=[tag])
    return render(response, "userprofile/course_tag_details.html", {'courses': courses, 'tag': tag})




