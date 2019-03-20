from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
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

    return render(request, 'societly/register.html', {'user_form':user_form,'student_form':student_form})
@login_required
def profile(request):
    context_dict = {}
    try:
        member = Student.objects.get(user=request.user)
        #member = Student.objects.get(matricNo = matricNo)
        context_dict['fullname'] = member.get_fullname(request.user)
        context_dict['matricNo'] = member.matricNo
        context_dict['degree'] = member.degree
        context_dict['societies'] = Society.objects.filter(member = matricNo)
        context_dict['memberships'] = len(list(memberships))
        context_dict['events'] = Event.objects.filter(attended_by = matricNo)
        context_dict['societies'] = None
        context_dict['memberships'] = None
        context_dict['events'] = None
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

def about_us(request):
    return render(request, "societly/about-us.html")

@login_required
def user_logout(request):
    logout(request)
    return render(request, "societly/home.html")

def contact_us(request):
    return render(request, "societly/contact-us.html")

def faq(request):
    return render(request, "societly/faq.html")

def log_in_form(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
                login(request,user)
                matricNo = Student.objects.filter(user=user)[0].matricNo
                #return HttpResponseRedirect(reverse('profile', args=[matricNo]))
                return HttpResponseRedirect(reverse('profile'))
    form = LogInForm()
    return render(request,'societly/LogIn.html',{'form':form})

def society(request,  society_name_slug):
    context_dict = {}
    try:
        society = Society.objects.get(slug = society_name_slug)
        events = Event.objects.filter(organized_by = society)
        context_dict['society'] = society
        context_dict['events'] = events
    except Exception as e:
        context_dict['society'] = None
        context_dict['events'] = None
        raise
    return render(request, "societly/society.html", context = context_dict)

@login_required
def event(request, eventId):
    context_dict = {}
    try:
        event = Event.objects.get(id = eventId)
        context_dict['name'] = event.name
        context_dict['date'] = event.date
        context_dict['time'] = event.time
        context_dict['description'] = event.description
        context_dict['image'] = event.image
        context_dict['organized_by'] = Society.organized_by.all()
        context_dict['attended_by'] = Student.attended_by.all()
    except:
        context_dict['name'] = None
        context_dict['date'] = None
        context_dict['time'] = None
        context_dict['description'] = None
        context_dict['image'] = None
        context_dict['organized_by'] = None
        context_dict['attended_by'] = None
    return render(request, "societly/event.html", context = context_dict)

def signup(request):
    return HttpResponse("Wanna join this shitty ass platform? Here is the fucking sign up page")

def add_event(request, matricNo):
    #function to add an event (by a society/board member of a society), make sure the function works if and only if
    #membership exists AND it is of type 'Board Member'
    return

    return render(request, "societly/profile.html", {
        'matricNo': matricNo,
        'fullname': fullname,
        'degree': degree,
        'memberships': membership_count,
        'societies': memberships,
        'events': events,
        'picture': picture
    })

@login_required 
def user_logout(request): 
    logout(request)
    return HttpResponseRedirect(reverse('index'))
