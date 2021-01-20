from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.urls import reverse


# Create your views here.

def index(request):
    return HttpResponse('OK')
