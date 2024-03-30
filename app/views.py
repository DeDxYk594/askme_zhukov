from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from django.core.paginator import Paginator

# Create your views here.



def index(request:HttpRequest)->HttpResponse:
    page_num=request.GET.get('page',1)
    paginator=Paginator(QUESTIONS,2,)
    page_obj=paginator.page(page_num)

    return render(request,"index.html",{"questions":page_obj})

def hot(request:HttpRequest)->HttpResponse:
    return render(request,"hot.html",{"questions":reversed(QUESTIONS)})

def question(request:HttpRequest,question_id)->HttpResponse:
    return render(request,"question.html",{"question":QUESTIONS[question_id]})
