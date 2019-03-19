from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Society, Event, Review, Membership 
from .forms import LogInForm,UserForm,StudentForm
from django.http import JsonResponse


# Create your views here.
def index(request):
    return render(request, "societly/home.html") 
    
def register(request):
    
    if request.method == 'POST':
    
        user_form = UserForm(data = request.POST)
        student_form = StudentForm(data = request.POST)
        
        if user_form.is_valid() and student_form.is_valid():
            user= user_form.save()
            user.set_password(user.password)
            user.save()
            
            student = student_form.save(commit=False)
            student.user = user
            
            if 'picture' in request.FILES:
                student.picture = request.FILES['picture']
            
            student.save()
            
            return log_in_form(request)
        
    else:
         user_form = UserForm()
         student_form = StudentForm()
    
    return render(request, 'socielty/register.html', {'user_form':user_form,'student_form':student_form})

def profile(request):
	societies = Society.objects.all()[:3]
	events = Event.objects.all()[:3]
	print(societies)
	print(events)
	student = request.user.get_username()
	context_dict =  {'societies':societies,'events':events, 'student' : student}
	return render(request, "societly/profile.html",context=context_dict) 

def about_us(request):
    return render(request, "societly/about-us.html")

def contact_us(request):
    return render(request, "societly/contact-us.html")

def faq(request):
    return render(request, "societly/faq.html")

def signup(request):
    return HttpResponse("Wanna join this shitty ass platform? Here is the fucking sign up page")
    
def log_in_form(request):

    if request.method == "POST":
        form = LogInForm(request.POST)

        username = request.POST.get('username')			
        password = request.POST.get('password')		
        user = authenticate(username=username,password=password)
			
        if user:
                login(request,user)
                return HttpResponseRedirect(reverse('profile'))
                
    form = LogInForm()
    return render(request,'societly/LogIn.html',{'form':form})

def society(request,  society_name_slug):
    context_dict = {}
    try:
        society = Society.objects.get(slug = society_name_slug)
        events = Event.objects.get(organized_by = society.name) 
        context_dict['society'] = society
        context_dict['events'] = events
        print(society)
    except:
        context_dict['society'] = None
        context_dict['events'] = None
    return render(request, "societly/society.html", context = context_dict)

@login_required
def profile_page(request, matricNo):
    context_dict = {}
    try:
        context_dict['fullname'] = member.get_fullname()
        context_dict['matricNo'] = member.matricNo
        context_dict['degree'] = member.degree
        context_dict['societies'] = Society.objects.filter(member = matricNo)
        context_dict['memberships'] = len(list(memberships))
        context_dict['events'] = Event.objects.filter(attended_by = matricNo)
        context_dict['picture'] = member.picture
    except:
        context_dict['fullname'] = None
        context_dict['matricNo'] = None
        context_dict['degree'] = None
        context_dict['societies'] = None
        context_dict['memberships'] = None
        context_dict['events'] = None
        context_dict['picture'] = None
    
    return render(request, "societly/profile.html", context = context_dict)
