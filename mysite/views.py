# mysite/views.py
from django.shortcuts import render
from django.http import HttpResponse

def homepage(request):
    return HttpResponse('여기는 218230085 김태연 홈 페이지 <a href="blog/">GO<a>')