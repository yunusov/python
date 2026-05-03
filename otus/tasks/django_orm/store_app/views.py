from django.http import HttpResponse
from django.shortcuts import render

def about(request):
    """Страница о нас"""
    return HttpResponse({"response": "about success"})

def index(request):
    """Страница index"""
    return HttpResponse({"response": "index success", "headers": ""})