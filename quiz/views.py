from django.shortcuts import render

from quiz.models import Question, QuestionList
from userprofile.models import Course
from .forms import QuestionForm
from django.shortcuts import redirect, get_object_or_404


# Create your views here.
def question_add(request):    
    if request.user.is_staff:
        form=QuestionForm()
        if(request.method=='POST'):
            form=QuestionForm(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('home')
        context={'form':form}
        return render(request,'quiz/addQuestion.html',context)
    else: 
        return redirect('home') 

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
            'questions':questions
        }
        return render(request,'quiz/quiz_detail.html',context)

#def quiz_detail(response,title):
 #   quiz = get_object_or_404(QuestionList, title=title)
  #  return render(response, "quiz/quiz_detail.html", {'quiz': quiz})

