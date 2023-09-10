from django.shortcuts import render
from django.http import HttpResponse


# Index View
def index(request):
    return render(request, 'index.html')


# About View
def about(request):
    return render(request, 'about.html')


# Contact View
def contact(request):
    return render(request, 'contact.html')


# Login View
def login(request):
    return render(request, 'login.html')



