from django.shortcuts import render
from django.http import JsonResponse, HttpResponse


# Create your views here.


def login(request):
    if request.method == 'POST':
        print(request.POST)
        print(type(request.POST))
        di = [{
            'username': 'zss',
            'password': 'safafg'
        }]

        return JsonResponse(di, safe=False)
