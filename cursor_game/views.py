from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from lazysignup.decorators import allow_lazy_user

@allow_lazy_user
def index(request):
    return render(request, 'the.html')
