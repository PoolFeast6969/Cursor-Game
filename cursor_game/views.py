from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from lazysignup.decorators import allow_lazy_user

@allow_lazy_user
def index(request):
    request.session['userid'] = request.META.get('HTTP_HOST', request.META.get('REMOTE_HOST', request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('HTTP_X_REAL_IP', request.META.get('REMOTE_ADDR', 'hacker')))))
    return render(request, 'the.html')
