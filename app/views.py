from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from django.core.paginator import Paginator

# Create your views here.

QUESTIONS=[
    {
        "id":0,
        "title":"Who is in this picture?",
        "text":"I though very long",
        "image":"img/president.jpg",
        "rating":5,
        "answers":[
            {
        "avatar":"img/president.jpg",
        "text":"Maybe, its president",
        "rating":2,
        "user":"mr_beast"
            }
        ]
        },
        
    {
        "id":1,
        "title": "What is the capital of France?",
        "text": "Test your geography knowledge",
        "image": "img/president.jpg",
        "rating": 4,
        "answers": [
            {
                "avatar": "img/president.jpg",
                "text": "The capital of France is Paris",
                "rating": 5,
                "user": "geo_expert"
            }
        ]
    },
    {
        "id":2,
        "title": "Who wrote the famous play 'Romeo and Juliet'?",
        "text": "A classic literary question",
        "image": "img/president.jpg",
        "rating": 4,
        "answers": [
            {
                "avatar": "img/president.jpg",
                "text": "William Shakespeare wrote 'Romeo and Juliet'",
                "rating": 5,
                "user": "bardfan"
            },
            {
                "avatar": "img/president.jpg",
                "text": "It was penned by an anonymous playwright",
                "rating": 4,
                "user": "literary_buff"
            }
        ]
    },
    {
        "id":3,
        "title": "What is the largest mammal on Earth?",
        "text": "Test your zoological knowledge",
        "image": "img/whale.jpg",
        "rating": 4,
        "answers": [
            {
                "avatar": "img/blue_whale.jpg",
                "text": "The largest mammal is the blue whale",
                "rating": 5,
                "user": "marine_biologist"
            },
            {
                "avatar": "img/elephant.jpg",
                "text": "It's the African elephant",
                "rating": 2,
                "user": "animal_lover"
            }
        ]
    },

]

def index(request:HttpRequest)->HttpResponse:
    page_num=request.GET.get('page',1)
    paginator=Paginator(QUESTIONS,2,)
    page_obj=paginator.page(page_num)

    return render(request,"index.html",{"questions":page_obj})

def hot(request:HttpRequest)->HttpResponse:
    return render(request,"hot.html",{"questions":reversed(QUESTIONS)})

def question(request:HttpRequest,question_id)->HttpResponse:
    return render(request,"question.html",{"question":QUESTIONS[question_id]})
