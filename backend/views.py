from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Society, Event, Review, Membership 
from .forms import LogInForm
from django.http import JsonResponse


# Create your views here.
def index(request):
    return render(request, "societly/home.html") 

def log_in_form(request):

    print("entered")
    if request.method == "POST":
        print("post")
        form = LogInForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            print("valid form")
            username = form.cleaned_data['username']			
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
			
            if user:
                print("access: ",user)
                login(request,user)
                return HttpResponseRedirect(reverse('profile'))
                
    print("reload")
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
