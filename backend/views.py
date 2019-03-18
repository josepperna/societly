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

@login_required
def profile_page(request, matricNo):
    member = Student.objects.filter(matricNo = matricNo)
    
    if member.user.is_authenticated():
        fullname = member.get_fullname()
        matricNo = member.matricNo
        degree = member.degree
        memberships = Society.objects.filter(member = matricNo)
        membership_count = len(list(memberships))
        events = Event.objects.filter(attended_by = matricNo)
        picture = member.picture

    return render(request, "societly/profile.html", {
        'matricNo': matricNo,
        'fullname': fullname,
        'degree': degree,
        'memberships': membership_count,
        'societies': memberships,
        'events': events,
        'picture': picture
    })