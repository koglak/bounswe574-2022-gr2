from django.shortcuts import render

from quiz.models import Case, CaseResult, Question, QuestionList, Score, CaseRating
from userprofile.models import Course
from .forms import CaseForm, QuestionForm, QuizForm, CaseResultForm, ScoreForm, CommentForm
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required

 
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
            return redirect('case_detail', title=case.title)
    return render(request, 'quiz/case_create.html', {'course': course, 'form':form})


@login_required(login_url="/login")
def case_detail(request,title):
    case=Case.objects.get(title=title)
    course=Course.objects.get(case_list=case)

    form= CaseResultForm()

    if request.method == 'POST':  
        form = CaseResultForm(request.POST, request.FILES)  
        if form.is_valid():  
            result = form.save(commit=False)
            result.user=request.user
            result.shared_date = timezone.now()
            result.case=case
            result.save()
            return redirect('course_detail', title=course.title)  
    else:  
        form= CaseResultForm()
        return render(request, 'quiz/case_detail.html', {'case':case, 'form': form, 'course': course})

@login_required(login_url="/login")
def case_list(response, title):
    startdate = datetime.today()
    enddate = startdate + timedelta(days=365)
    case=get_object_or_404(Case, title=title)
    case_list= Event.objects.filter(case=case, event_date__range=[startdate, enddate])


    form_date=DateFilterForm(response.POST or None)

    if response.method == "POST":
        # Date Sorting
        if 'published_date' in response.POST:
                form_date=DateFilterForm(response.POST)
                print("published_date")
                if form_date.is_valid():
                    print("valid")
                    date_filter= response.POST['published_date']
                    print(date_filter)
                    if date_filter =="Ascending":
                        print("here")
                        case_list= Event.objects.filter(course=course, case_date__range=[startdate, enddate]).order_by('published_date__day', 'published_date__month')
                    else:
                        print("else")
                        event_list= Event.objects.filter(course=course, event_date__range=[startdate, enddate]).order_by('-event_date__day', '-event_date__month')
        # Keyword Search
        else:
            searched = response.POST["case_searched"]
            event_list=Event.objects.filter(course=course, title__icontains=searched, event_date__range=[startdate, enddate])
            form = CategorySortingForm(use_required_attribute=False)
            form_date=DateFilterForm(use_required_attribute=False)

    paginator = Paginator(case_list,3) 
    page = response.GET.get('page')
    cases= paginator.get_page(page)

    return render(response, "userprofile/case_page.html", {'course': course, 'case':case, "form": form, "form_date": form_date})


@login_required(login_url="/login")
def case_grade(request,title):
    case=Case.objects.get(title=title)
    ListFormSet = modelformset_factory(CaseResult, fields=('score',), extra=0)
    if request.method == 'POST':
        list_formset = ListFormSet(request.POST)
        if list_formset.is_valid():
            list_formset.save()
            return redirect('case_grade', title=case.title)  
    else: 
        list_formset = ListFormSet(queryset=CaseResult.objects.filter(case=case).order_by('shared_date'))
        course=Course.objects.get(case_list=case)
        return render(request, 'quiz/case_grade.html', {'list_formset': list_formset, 'course':course} )

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

def comment_new(request):
    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()

            return redirect(reverse('quiz/case_detail.html', kwargs = {
                'pk' : post.pk
            })) 
 
    return render(request, 'quiz/case_detail.html', {'form': form,'pk': pk})

def comment_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m() 

            return redirect('case_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'quiz/case_edit.html', {'form': form, 'pk': pk})

def delete_comment(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('/comment')

@login_required(login_url="/login")
def LikeView_comment(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    post.dislikes.remove(request.user)
    return redirect('case_detail', pk=pk)


@login_required(login_url="/login")
def LikeViewList_comment(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    post.dislikes.remove(request.user)
    return redirect('comment')


@login_required(login_url="/login")
def DislikeView_comment(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.dislikes.add(request.user)
    post.likes.remove(request.user)
    return redirect('case_detail', pk=pk)


@login_required(login_url="/login")
def DislikeViewList_comment(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.dislikes.add(request.user)
    post.likes.remove(request.user)
    return redirect('case_page')

@login_required(login_url="/login")
def ReplyCommentLikeView(request, pk):
    answer = get_object_or_404(Answer, id=request.POST.get('answer_id'))
    answer.likes.add(request.user)
    answer.dislikes.remove(request.user)
    return redirect('case_detail', pk=pk)


@login_required(login_url="/login")
def ReplyCommentDislikeView(request,pk ):
    answer = get_object_or_404(Answer, id=request.POST.get('answer_id'))
    answer.dislikes.add(request.user)
    answer.likes.remove(request.user)
    return redirect('case_detail', pk=pk)

