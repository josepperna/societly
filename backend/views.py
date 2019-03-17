from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student, Society, Event, Review, Membership 
from .forms import LogInForm
from django.http import JsonResponse

# Create your views here.
def index(request):
    new_events = Event.objects.order_by('-date')[:10]
    context_dict = {'new_events' : new_events}
    return render(request, "societly/home.html",context=context_dict) 

def log_in_form(request):
	registered = False
	
	if request.method == 'POST':
		form = LogInForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('societly/profile/')
			
	else:
			
		form = LogInForm()
	return render(request,'societly/LogIn.html',{'form':form})

def profile(request):
	societies = Society.objects.all()[:3]
	events = Event.objects.all()[:3]
	print(societies)
	print(events)
	student = request.user.get_username()
	context_dict =  {'societies':societies,'events':events, 'student' : student}
	return render(request, "societly/profile.html",context=context_dict) 
    
def about_us(request):
    return HttpResponse("Hello again, this is the fucking about us page")

def contact_us(request):
    return HttpResponse("Hello again bitch, this is the fucking contact us page")

def faq(request):
    return HttpResponse("Got some questions? Here are the fucking answers")

def signup(request):
    return HttpResponse("Wanna join this shitty ass platform? Here is the fucking sign up page")
