from django.shortcuts import render

from quiz.models import Question, QuestionList
from userprofile.models import Course
from .forms import QuestionForm, QuizForm
from django.shortcuts import redirect, get_object_or_404


# Create your views here.
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
        context = {
            'score':score,
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total
        }
        return render(request,'quiz/quiz_result.html',context)
    else:
        quiz = get_object_or_404(QuestionList, title=title)
        questions=quiz.question_list.all()
        context = {
            'quiz': quiz,
            'questions':questions
        }
        return render(request,'quiz/quiz_detail.html',context)

#def quiz_detail(response,title):
 #   quiz = get_object_or_404(QuestionList, title=title)
  #  return render(response, "quiz/quiz_detail.html", {'quiz': quiz})

def quiz_create(request, title):
    course = get_object_or_404(Course, title=title)
    
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

def question_add(request,title):    
    if request.user.is_staff:
        form=QuestionForm()
        ###
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
    else: 
        return redirect('quiz_detail', title=title) 