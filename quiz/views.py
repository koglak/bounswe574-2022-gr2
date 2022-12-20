from django.shortcuts import render

from quiz.models import Case, CaseResult, Question, QuestionList, Score, CaseRating
from userprofile.models import Course
from .forms import CaseForm, QuestionForm, QuizForm, CaseResultForm, ScoreForm, CommentForm
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
#from hitcount.views import HitCountDetailView


 
# Create your views here.
@login_required(login_url="/login")
def quiz_detail(request,title):
    if request.method == 'POST':
        print(request.POST)
        quiz = get_object_or_404(QuestionList, title=title)
        questions=quiz.question_list.all()
        score=0
        wrong=0
        correct=0
        total=0
        for q in questions:
            total+=1
            print(request.POST.get(q.question))
            print(q.ans)
            print()
            if q.ans ==  request.POST.get(q.question):
                score+=10
                correct+=1
            else:
                wrong+=1
        percent = score/(total*10) *100
        user_score=Score.objects.create(user=request.user, quiz=quiz, score=percent)
        course= Course.objects.get(question_list__pk=quiz.pk)

        context = {
            'score':score,
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total,
            'course':course
        }
        return render(request,'quiz/quiz_result.html',context)
    else:
        quiz = QuestionList.objects.get(title=title)
        questions=quiz.question_list.all()
        course= Course.objects.get(question_list__pk=quiz.pk)
        
        context = { 
            'quiz': quiz,
            'questions':questions,
            'course':course
        }
        return render(request,'quiz/quiz_detail.html',context)

#def quiz_detail(response,title):
 #   quiz = get_object_or_404(QuestionList, title=title)
  #  return render(response, "quiz/quiz_detail.html", {'quiz': quiz})


@login_required(login_url="/login")
def quiz_create(request, title):
    course=Course.objects.get(title=title)    
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.user = request.user
            quiz.course = course
            quiz.save()
            return redirect('quiz_detail', title=quiz.title)
    else:
        form = QuizForm()
        return render(request, 'quiz/quiz_create.html', {'form': form, 'title': title})


@login_required(login_url="/login")
def question_add(request,title):    
    form=QuestionForm()
    quiz = QuestionList.objects.get(title=title)
        
    if request.method=='POST':
        form=QuestionForm(request.POST)
        if form.is_valid():
            question=form.save(commit=False)
            question.save()
            quiz.question_list.add(question.pk)
            quiz.save()

            return redirect('quiz_detail', title=title)

    context={'form':form}
    return render(request,'quiz/question_add.html',context)
   

@login_required(login_url="/login")
def quiz_delete(request, title):
    quiz = QuestionList.objects.get(title=title)
    course= Course.objects.get(question_list__pk=quiz.pk)

    quiz.delete()
    return redirect('course_detail', title=course.title)


@login_required(login_url="/login")
def case_create(request,title):
    course=Course.objects.get(title=title)
    form = CaseForm()
    if request.method == "POST":
        form = CaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.user = request.user
            case.course = course
            case.save()
            return redirect('case_list', title=case.course.title)

    return render(request, 'quiz/case_create.html', {'course': course, 'form':form})

@login_required(login_url="/login")
def case_edit(request, title):
    case = get_object_or_404(Case, title=title)
    if request.method == "POST":
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.user=request.user
            instance.save()
            return redirect('case_list', title=case.course.title)
    else:
        form = CaseForm(instance=case)
    return render(request, 'quiz/case_edit.html', {'form': form, 'title': case.title})

@login_required(login_url="/login")
def case_delete(request, title):
    case = get_object_or_404(Case, title=title)
    case.delete()
    return redirect('case_list', title=case.course.title)

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

    return render(response, "quiz/case_list.html", {'course': course, ' cases': cases, "form_date": form_date})


@login_required(login_url="/login")
def case_detail(response, title):
    case = Case.objects.get(title=title)
    ListFormSet = modelformset_factory(CaseResult, fields=('score',), extra=0)
    if response.method == "POST":
        form = CommentForm(response.POST)
        if form.is_valid():

            comment = form.save(commit=False)
            comment.case = case
            comment.author = response.user
            comment.save()
            form = CommentForm()
        else:
            list_formset.save()
            return redirect('case_detail', title=case.title)  
    else:
        form = CommentForm()
    context = {
        'course': case.course,
        'case': case,
        #'enrolled_users': Case.enrolled_users.through.objects.all(),
        'form': form,
    }

    return render(response, "quiz/case_detail.html", context)

# def upload_work(request, title):
#     case = Case.objects.get(title = title)
#     course = Course.objects.get(case_list, case)

#     form = CaseResultForm()

#     if request.method == 'POST':
#         form = CaseResultForm(request.POST, request.FILES)
#         if form.is_valid():
#             result = form.save(commit=False)
#             result.user = request.user
#             resul.shared_date = timezone.now()
#             result.case = case
#             result.save()
#             return redirect('case_grade', title = case.title)

#     else:
#         form = CaseResultForm()
#         return render(request, 'quiz/case_grade.html', {'case':case, 'form':form, 'course':course})

@login_required(login_url="/login")
def case_grade(request,title):
    case=Case.objects.get(title=title)
    ListFormSet = modelformset_factory(CaseResult, fields=('score',), extra=0)
    if request.method == 'POST':
        list_formset = ListFormSet(request.POST)
        form = CaseResultForm(request.POST, request.FILES) 
        if list_formset.is_valid():
            list_formset.save()
            return redirect('case_grade', title=case.title)  
    else: 
        list_formset = ListFormSet(queryset=CaseResult.objects.filter(case=case).order_by('shared_date'))
        course=Course.objects.get(case_list=case)
        return render(request, 'quiz/case_grade.html', {'list_formset': list_formset, 'course':course} )

def submit_assignment(request, title):
    case=Case.objects.get(title=title)
    course=Course.objects.get(case_list=case)
    form = CaseResultForm()
    if request.method == 'POST':  
        form = CaseResultForm(request.POST, request.FILES)  
        if form.is_valid():  
            result = form.save(commit=False)
            result.user=request.user
            result.shared_date = timezone.now()
            result.case=case
            result.save()
            return redirect('case_grade', title=course.title)  
    else:  
        form= CaseResultForm()
        return render(request, 'quiz/submit_assignment.html', {'case':case, 'form': form, 'course': course})


# def delete_submission(request, title):
#     case = get_object_or_404(Case, title=title)
#     case.delete()
#     return redirect('delete_submission', title=case.course.title)



@login_required(login_url="/login")
def case_rate(request, pk):
    case_result = get_object_or_404(CaseResult, pk=pk)
    case=case_result.case
    if request.method == 'POST':
        rating=request.POST["rating"]
        print(rating)
        if case_result.caserating_set.filter(user=request.user, rating=rating ):
            print('already rated')
        elif case_result.caserating_set.filter(user=request.user):
            obj= CaseRating.objects.get(user=request.user, case_result=case_result)
            obj.rating = rating
            obj.save()
            case_result.averagereview()
        else:
            obj = CaseRating.objects.create(case_result=case_result, user=request.user, rating=rating)
            obj.save()
            case_result.averagereview()

    return redirect('case_grade', title=case.title)

def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.delete()
    return redirect('comment_detail')

def search_case(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        results = Case.objects.filter(title__icontains=searched)

        return render(request, "quiz/search_case.html", {'searched': searched, 'results': results}) 
    else:
        return render(request, "quiz/search_case.html", {})