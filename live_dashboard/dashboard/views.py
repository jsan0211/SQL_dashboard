from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Hello from your Dashboard App!</h1>")

# Create your views here.
