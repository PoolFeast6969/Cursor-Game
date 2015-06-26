from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def index(request):
    request.session['ip'] = request.META.get('HTTP_HOST', request.META.get('REMOTE_HOST', request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('HTTP_X_REAL_IP', request.META.get('REMOTE_ADDR', 'hacker')))))
    return render(request, 'the.html')
