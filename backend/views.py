from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student, Society, Event, Review, Membership

# Create your views here.
def index(request):
    return render(request, "societly/index.html") 

def about_us(request):
    return HttpResponse("Hello again, this is the fucking about us page")

def contact_us(request):
    return HttpResponse("Hello again bitch, this is the fucking contact us page")

def faq(request):
    return HttpResponse("Got some questions? Here are the fucking answers")

def signup(request):
    return HttpResponse("Wanna join this shitty ass platform? Here is the fucking sign up page")