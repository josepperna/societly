from django.shortcuts import render
from django.http import HttpResponse
from .models import Student, Society, Event, Review, Membership

# Create your views here.
def index(request):
    return HttpResponse("Hello, this is the fucking Index Page")

def society_page(request):
    return HttpResponse("Hello again, this is the fucking Society Page")