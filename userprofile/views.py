
# Create your views here.
import json
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render
from blog.models import Post
from quiz.models import Case, Question, QuestionList, Score
from .models import Course, Profile, Rating, Lecture, Event, Question, Answer
from .forms import CourseForm, ProfileForm, LectureForm, EventForm, CategorySortingForm, DateFilterForm, CommentsForm, QuestionForm, AnswerForm
from django.shortcuts import redirect, get_object_or_404
from taggit.models import Tag
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, time
from django.core.paginator import Paginator
from django.urls import reverse


@login_required(login_url="/login")
def user_profile(response):
    print(response.user)
    courses=Course.objects.filter(user = response.user).order_by('published_date')
    user_profile = get_object_or_404(Profile, user=response.user)
    collaborative_member=Course.objects.filter(collaborative_members = response.user)
    question=Post.objects.filter(author=response.user)
    return render(response, "userprofile/profile.html", {'courses':courses, 'user_profile':user_profile, 'collaborative_member': collaborative_member, 'question':question})

@login_required(login_url="/login")
def course_detail(request, title):
    course =Course.objects.get(title=title)
    score_list = Score.objects.filter(user=request.user)
    context = {
            'course': course,
            'score_list':score_list,
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

@login_required(login_url="/login")
def delete_course(request, title):
    course = Course.objects.get(title=title)
    course.delete()
    return redirect('/myspace/profile')

@login_required(login_url="/login")
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

    return redirect('course_detail', title=course.title)

@login_required(login_url="/login")
def other_user_profile(response, name):
    courses=Course.objects.filter(user__username=name).order_by('published_date')
    user_profile=Profile.objects.get(user__username=name)
    collaborative_member=Course.objects.filter(collaborative_members__username = name)
    question=Post.objects.filter(author=user_profile.user)
    name = response.GET.get('name')
    if name=="follow":
        user_profile.followers.add(response.user)
    elif name=="unfollow":
        user_profile.followers.remove(response.user)

    return render(response, "userprofile/profile.html", {'courses': courses, 'user_profile': user_profile, 'collaborative_member': collaborative_member, 'question': question})




@login_required(login_url="/login")
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

@login_required(login_url="/login")
def lecture_detail(response, pk):
    lecture = get_object_or_404(Lecture, pk=pk)
    course = Course.objects.get(lecture__title=lecture.title)
    score_list = Score.objects.filter(user=response.user)

    context = {
            'course': course,
            'lecture': lecture,
            'score_list':score_list,
        }

    return render(response, "userprofile/lecture_detail.html",context)

@login_required(login_url="/login")
def search_course(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        results = Course.objects.filter(title__icontains=searched)

        return render(request, "userprofile/search_course.html", {'searched': searched, 'results': results}) 
    else:
        return render(request, "userprofile/search_course.html", {}) 

@login_required(login_url="/login")
def course_enroll(request,pk):
    course = get_object_or_404(Course, pk=pk)

    course.enrolled_users.add(request.user)
    title=course.title
    
    return redirect('course_detail', title=title)

@login_required(login_url="/login")
def course_drop(request,pk):
    course = get_object_or_404(Course, pk=pk)

    course.enrolled_users.remove(request.user)
    title=course.title
    
    return redirect('course_detail', title=title)


@login_required(login_url="/login")
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

@login_required(login_url="/login")
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


@login_required(login_url="/login")
def delete_lecture(request, title):
    lecture = Lecture.objects.get(title=title)
    course= Course.objects.get(lecture__pk=lecture.pk)

    lecture.delete()
    return redirect('course_detail', title=course.title)

@login_required(login_url="/login")
def learn_page(response):
    course = Course.objects.filter(enrolled_users=response.user)
    return render(response, "userprofile/learn.html", {'course': course})

@login_required(login_url="/login")
def event_list(response, title):
    startdate = datetime.today()
    enddate = startdate + timedelta(days=365)
    course=get_object_or_404(Course, title=title)
    event_list= Event.objects.filter(course=course, event_date__range=[startdate, enddate])

    form = CategorySortingForm(response.POST or None)
    form_date=DateFilterForm(response.POST or None)

    if response.method == "POST":
        # Category Filtering
        if 'category' in response.POST:
            form = CategorySortingForm(response.POST)
            if form.is_valid():
                filtered_category = response.POST['category']                
                if filtered_category!="All" :
                    event_list = Event.objects.filter(course=course,category=filtered_category, event_date__range=[startdate, enddate])
                else:
                    event_list = Event.objects.filter(course=course, event_date__range=[startdate, enddate])
        # Date Sorting
        elif 'event_date' in response.POST:
                form_date=DateFilterForm(response.POST)
                form= CategorySortingForm(use_required_attribute=False)
                print("event_date")
                if form_date.is_valid():
                    print("valid")
                    date_filter= response.POST['event_date']
                    print(date_filter)
                    if date_filter =="Ascending":
                        print("here")
                        event_list= Event.objects.filter(course=course, event_date__range=[startdate, enddate]).order_by('event_date__day', 'event_date__month')
                    else:
                        print("else")
                        event_list= Event.objects.filter(course=course, event_date__range=[startdate, enddate]).order_by('-event_date__day', '-event_date__month')
        # Keyword Search
        else:
            searched = response.POST["searched"]
            event_list=Event.objects.filter(course=course, title__icontains=searched, event_date__range=[startdate, enddate])
            form = CategorySortingForm(use_required_attribute=False)
            form_date=DateFilterForm(use_required_attribute=False)
    # No post request
    else:
        form = CategorySortingForm(initial={'category': "All"})
        form_date=DateFilterForm(use_required_attribute=False)

    paginator = Paginator(event_list,3) 
    page = response.GET.get('page')
    events= paginator.get_page(page)

    return render(response, "userprofile/event_list.html", {'course': course, 'events':events, "form": form, "form_date": form_date})

@login_required(login_url="/login")
def past_event(response, title):
    enddate = datetime.today()
    startdate = enddate - timedelta(days=365)
    course=get_object_or_404(Course, title=title)
    event_list= Event.objects.filter(course=course, event_date__range=[startdate, enddate]).order_by('-event_date')
    form = CategorySortingForm(response.POST)
    
    if response.method == "POST":
        if form.is_valid():
            filtered_category = response.POST['category']                
            if filtered_category!="All" :
                event_list = Event.objects.filter(course=course,category=filtered_category, event_date__range=[startdate, enddate])
        else:
            searched = response.POST["searched"]
            event_list=Event.objects.filter(course=course, title__icontains=searched, event_date__range=[startdate, enddate])
            form = CategorySortingForm( use_required_attribute=False)
    else:
        form = CategorySortingForm(initial={'category': "All"})
    
    paginator = Paginator(event_list,3) 
    page = response.GET.get('page')
    events= paginator.get_page(page)

    return render(response, "userprofile/event_list.html", {'course': course, 'events':events, "form": form})

@login_required(login_url="/login")
def quiz_page(response, title):
    course=get_object_or_404(Course, title=title)
    score_list = Score.objects.filter(user=response.user)
    return render(response, "userprofile/quiz_page.html", {'course': course, 'score_list': score_list})

@login_required(login_url="/login")
def case_page(response, title):
    course=get_object_or_404(Course, title=title)
    score_list = Score.objects.filter(user=response.user)
    return render(response, "userprofile/case_page.html", {'course': course, 'score_list': score_list})

@login_required(login_url="/login")
def case_list(response, title):
    startdate = datetime.today()
    enddate = startdate + timedelta(days=365)
    course=get_object_or_404(Course, title=title)
    case_list= Case.objects.filter(course=course, published_date__range=[startdate, enddate])

    form_date=DateFilterForm(response.POST or None)

    if response.method == "POST":
        # Date Sorting
        if 'published_date' in response.POST:
                form_date=DateFilterForm(response.POST)
                if form_date.is_valid():
                    date_filter= response.POST['published_date']
                    if date_filter =="Ascending":
                        case_list= Case.objects.filter(course=course, case_date__range=[startdate, enddate]).order_by('published_date__day', 'published_date__month')
    # No post request
    else:
        form_date=DateFilterForm(use_required_attribute=False)

    paginator = Paginator(case_list,10) 
    page = response.GET.get('page')
    cases= paginator.get_page(page)

    return render(response, "userprofile/case_list.html", {'course': course, ' cases': cases, "form_date": form_date})

@login_required(login_url="/login")
def case_page(response, title):
    course=get_object_or_404(Course, title=title)
    score_list = Score.objects.filter(user=response.user)
    return render(response, "userprofile/case_page.html", {'course': course, 'score_list': score_list})

@login_required(login_url="/login")
def case_inprogress_list(response, title):
    startdate = datetime.today()
    enddate = startdate + timedelta(days=365)
    course=get_object_or_404(Course, title=title)
    case_list= Case.objects.filter(course=course, due_date__range=[startdate, enddate])

    form_date=DateFilterForm(response.POST or None)

    if response.method == "POST":
        # Date Sorting
        if 'due_date' in response.POST:
                form_date=DateFilterForm(response.POST)
                if form_date.is_valid():
                    date_filter= response.POST['due_date']
                    if date_filter =="Ascending":
                        case_list= Case.objects.filter(course=course, case_date__range=[startdate, enddate]).order_by('-due_date__day', '-due_date__month')
    # No post request
    else:
        form_date=DateFilterForm(use_required_attribute=False)

    paginator = Paginator(case_list,10) 
    page = response.GET.get('page')
    cases= paginator.get_page(page)

    return render(response, "userprofile/case_inprogress_list.html", {'course': course, ' cases': cases, "form_date": form_date})

login_required(login_url="/login")
def case_closed_list(response, title):
    enddate = datetime.today()
    startdate = enddate - timedelta(days=365)
    course=get_object_or_404(Course, title=title)
    case_list= Case.objects.filter(course=course, due_date__range=[startdate, enddate]).order_by('-due_date')
    
    if response.method == "POST":
        if form.is_valid():
            searched = response.POST["searched"]
            case_list=Case.objects.filter(course=course, title__icontains=searched, due_date__range=[startdate, enddate])
    
    paginator = Paginator(case_list,10) 
    page = response.GET.get('page')
    cases= paginator.get_page(page)

    return render(response, "userprofile/case_closed_list.html", {'course': course, 'cases':cases})

@login_required(login_url="/login")
def event_new(request, title):
    course=get_object_or_404(Course, title=title)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.course=course
            event.published_date = timezone.now()
            event.save()
            return redirect('event_list', title=title)
    else:
        form = EventForm()
        pk ="none"
    return render(request, 'userprofile/event_edit.html', {'form': form, 'pk':pk})


@login_required(login_url="/login")
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.user=request.user
            instance.save()
            return redirect('event_list', title=event.course.title)
    else:
        form = EventForm(instance=event)
    return render(request, 'userprofile/event_edit.html', {'form': form, 'pk': event.pk})

@login_required(login_url="/login")
def event_enroll(request,pk):
    event = get_object_or_404(Event, pk=pk)
    event.enrolled_users.add(request.user)
    return redirect('event_list', title=event.course.title)

@login_required(login_url="/login")
def delete_event(request, pk):
    event = Event.objects.get(pk=pk)
    event.delete()
    return redirect('event_list', title=event.course.title)


@login_required(login_url="/login")
def event_detail(response, pk):
    event = Event.objects.get(pk=pk)
    if response.method == "POST":
        form = CommentsForm(response.POST)
        if form.is_valid():

            comment = form.save(commit=False)
            comment.event = event
            comment.user = response.user
            comment.save()
            form = CommentsForm()
    else:
        form = CommentsForm()
    context = {
        'course': event.course,
        'event': event,
        'enrolled_users': Event.enrolled_users.through.objects.all(),
        'form': form,
    }

    return render(response, "userprofile/event_detail.html", context)

@login_required(login_url="/login")
def forum_page(response, title):
    course=get_object_or_404(Course, title=title)
    questions= Question.objects.filter(course=course).order_by('-published_date')
    paginator = Paginator(questions,3) 
    page = response.GET.get('page')
    question_list= paginator.get_page(page)
    return render(response, 'userprofile/forum_page.html', {'course': course, 'questions': question_list})

@login_required(login_url="/login")
def question_new(request,title):
    if request.method == "POST":
        course=get_object_or_404(Course, title=title)
        questions= Question.objects.filter(course=course).order_by('-published_date')
        form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.course = course
            question.published_date = timezone.now()
            question.save()

            return redirect('forum_page', {'course': course, 'questions': questions})
    else:
        form = QuestionForm()
        pk ="none"
    return render(request, 'userprofile/question_edit.html', {'form': form,'pk': pk})


@login_required(login_url="/login")
def question_detail(request, pk, title):
    course=get_object_or_404(Course, title=title)
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.user = request.user
            answer.published_date = timezone.now()
            answer.save()
    else:
        form = AnswerForm()
    return render(request, 'userprofile/question_detail.html', {'question': question, "form":form, "course": course})

@login_required(login_url="/login")
def question_edit(request, pk, title):
    course=get_object_or_404(Course, title=title)
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.course = course
            question.published_date = timezone.now()
            question.save()
            form.save_m2m()

            return redirect(f'/myspace/{course.title}/forum_page/{question.pk}')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'userprofile/question_edit.html', {'form': form, 'pk': pk, "course": course, "question": question})

@login_required(login_url="/login")
def LikeView(request, pk, title):
    question = get_object_or_404(Question, pk=pk)
    question.likes.add(request.user)
    question.dislikes.remove(request.user)
    return redirect(f'/myspace/{title}/forum_page/{pk}')

@login_required(login_url="/login")
def DislikeView(request, pk, title):
    question = get_object_or_404(Question, pk=pk)
    question.dislikes.add(request.user)
    question.likes.remove(request.user)
    return redirect(f'/myspace/{title}/forum_page/{pk}')

@login_required(login_url="/login")
def AnswerLikeView(request, pk, title,num):
    answer = get_object_or_404(Answer, pk=num)
    answer.likes.add(request.user)
    answer.dislikes.remove(request.user)
    return redirect(f'/myspace/{title}/forum_page/{pk}')


@login_required(login_url="/login")
def AnswerDislikeView(request,pk,title,num ):
    answer = get_object_or_404(Answer, pk=num)
    answer.dislikes.add(request.user)
    answer.likes.remove(request.user)
    return redirect(f'/myspace/{title}/forum_page/{pk}')


@login_required(login_url="/login")
def LikeViewList(request, pk, title):
    question = get_object_or_404(Question, pk=pk)
    question.likes.add(request.user)
    question.dislikes.remove(request.user)
    return redirect("forum_page", title=title)

@login_required(login_url="/login")
def DislikeViewList(request, pk, title):
    question = get_object_or_404(Question, pk=pk)
    question.likes.remove(request.user)
    question.dislikes.add(request.user)
    return redirect("forum_page", title=title)

@login_required(login_url="/login")
def delete_question(request, pk, title):
    question = Question.objects.get(pk=pk)
    question.delete()
    return redirect("forum_page", title=title)

@login_required(login_url="/login")
def search_question(request, title):
    course=get_object_or_404(Course, title=title)
    if request.method == "POST":
        searched = request.POST["searched"]
        results=Question.objects.filter(course=course, title__icontains=searched)

        return render(request, 'userprofile/forum_page.html', {'course': course, 'questions': results}) 
    else:
        return render(request, "userprofile/forum_page.html", {'course': course}) 

@login_required(login_url="/login")
def metric_pages(request, title):
    course=get_object_or_404(Course, title=title)
    
    return render(request, "userprofile/space_metrics.html", {"course":course}) 

def save_annotation(request):
    context=request.GET["context"]
    types=request.GET["type"]
    id=request.GET["id"]
    target=request.GET["target"]
    body=request.GET["body"]

    annotation={
        "@context": json.loads(context),
        "body": [json.loads(body)],
        "id": "#" + json.loads(id),
        "target":json.loads(target),
        "type":json.loads(types)
    }

    print(annotation)
    print("working...")

    res = HttpResponse("successful")
    return res

