from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Society, Event, Review, Membership
from .forms import LogInForm,UserForm,StudentForm, EventForm
import datetime

# Create your views here.
#Homepage view if the user is not logged in, profile page view otherwise
def index(request):
    if request.user and request.user.is_authenticated:
        return profile(request)
    else:
        return render(request, "societly/home.html")

#View to show all societies in the database
def show_all_societies(request):
    societies = Society.objects.all()
    context_dict = {'societies': societies}
    return render(request, 'societly/Show_all_societies.html', context_dict)

#View to show all the societies the current logged in user is member of
@login_required
def show_your_societies(request):
    student = Student.objects.filter(user = request.user)
    societies = Membership.objects.filter(member = student)
    context_dict = {'societies': societies}
    return render(request, 'societly/showmysocieties.html', context_dict)

#Show all events in the database
def show_all_events(request):
    events = Event.objects.all()
    context_dict = {'events': events}
    return render(request, 'societly/show_all_events.html', context_dict)

#Show all events attended/to be attended by the current user
@login_required
def show_your_events(request):
    student = Student.objects.filter(user = request.user)
    events = Event.objects.filter(attended_by = student)
    context_dict = {'events': events}
    return render(request, 'societly/showmyevents.html', context_dict)

#View to sign up with a new account
def register(request):

    if request.method == 'POST':
        print("aa")
        user_form = UserForm(data = request.POST)
        student_form = StudentForm(request.POST, request.FILES)

        if user_form.is_valid() and student_form.is_valid():
            user= user_form.save()
            user.set_password(user.password)
            user.save()

            student = student_form.save(commit=False)
            student.user = user
            student.picture = student_form.cleaned_data['picture']

            student.save()

            return log_in_form(request)

    else:
         user_form = UserForm()
         student_form = StudentForm()

    return render(request, 'societly/register.html', {'user_form':user_form,'student_form':student_form})

#def register_society(request):
#    if request.method == 'POST':
#            society_form = StudentForm(data = request.POST)
#
#            if scoeity_form.is_valid():
#                society = society_form.save(commit=False)
#
#                if 'logo' in request.FILES:
#                    print("logo exists")
#                    society.picture = request.FILES['logo']
#
#                society.save()
#
#
#                return log_in_form(request)
#
#       else:
#            society_form = RegisterSocietyForm()
#
#        return render(request, 'societly/registerSociety.html', {'society_form':society_form})

#View to get profile information
@login_required
def profile(request):
    context_dict = {}
    try:
        member = Student.objects.get(user=request.user)
        context_dict['fullname'] = member.get_fullname(request.user)
        context_dict['matricNo'] = member.matricNo
        context_dict['degree'] = member.degree
        context_dict['societies'] =  Membership.objects.filter(member = member).order_by('-date_joined')[:3]
        context_dict['events'] = Event.objects.filter(attended_by = member).order_by('-date')[:3]
        context_dict['picture'] = member.picture
    except Exception as e:
        print(e)
        context_dict['fullname'] = None
        context_dict['matricNo'] = None
        context_dict['degree'] = None
        context_dict['societies'] = None
        context_dict['events'] = None
        context_dict['picture'] = None

    return render(request, "societly/profile.html", context = context_dict)

#About us page view
def about_us(request):
    return render(request, "societly/about-us.html")

#Contact us page view
def contact_us(request):
    return render(request, "societly/contact-us.html")

#Frequently asked questions page view
def faq(request):
    return render(request, "societly/faq.html")

#View to login a registered user
def log_in_form(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
                login(request,user)
                matricNo = Student.objects.filter(user=user)[0].matricNo
                return HttpResponseRedirect(reverse('profile'))
    form = LogInForm()
    return render(request,'societly/LogIn.html',{'form':form})

#View to see a specific societies info
def society(request, society_name_slug):
    context_dict = {}
    try:
        society = Society.objects.filter(slug = society_name_slug.lower()).first()
        events = Event.objects.filter(organized_by = society)
        context_dict['society'] = society
        context_dict['events'] = events
        if request.user.is_authenticated:
            member = Student.objects.get(user=request.user)
            if len(Membership.objects.filter(member = member, society = society)) != 0:
                context_dict['member'] = True
            else:
                context_dict['member'] = False
        else:
            context_dict['member'] = False
    except Exception as e:
        print(e)
        context_dict['society'] = None
        context_dict['events'] = None
        context_dict['member'] = False
    return render(request, "societly/society.html", context = context_dict)

#View to see a specific event's info
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
        context_dict['organized_by'] = event.organized_by.all()[0]
        context_dict['participants'] = event.attended_by.all()
        #context_dict['attending'] = event.attended_by_set.
    except Exception as e:
        print(e)
        context_dict['name'] = None
        context_dict['date'] = None
        context_dict['time'] = None
        context_dict['description'] = None
        context_dict['image'] = None
        context_dict['organized_by'] = None
        context_dict['participants'] = None
    return render(request, "societly/event.html", context = context_dict)

#View to add a new event to a specific societies list of events
@login_required
def add_event(request, society_name_slug):
    if request.method == 'POST':
        event_form = EventForm(request.POST, request.FILES)
        society = Society.objects.filter(slug = society_name_slug)
        if event_form.is_valid():
            ev = event_form.save()
            ev.organized_by = society
            ev.image = event_form.cleaned_data['image']
            ev.save()
            return event(request, ev.id)

    else:
        event_form = EventForm()

    return render(
        request,
        'societly/addEvent.html',
        {
            'event_form': event_form,
        }
    )

#View to logout and redirect to the home page
@login_required 
def user_logout(request): 
    logout(request)
    return HttpResponseRedirect(reverse('index'))

#View to subscribe to a society
@login_required
def subscribe_to_society(request):
    if request.method == 'GET':
        society_slug = request.GET['society']
        society = Society.objects.get(slug = society_slug.lower())
        if society:
            Membership.objects.get_or_create(society=society ,member=Student.objects.get(user=request.user))
    return HttpResponse()

#View to delete a membership of a society
@login_required
def unsubscribe_from_society(request):
    if request.method == 'GET':
        society_slug = request.GET['society']
        society = Society.objects.get(slug = society_slug.lower())
        if society:
            Membership.objects.filter(society=society, member=Student.objects.get(user=request.user)).delete()
    return HttpResponse()

#View to attend an event
@login_required
def attendEvent(request):
    if request.method == 'GET':
        society_slug = request.GET['society']
        society = Society.objects.get(slug = society_slug.lower())
        if society:
            Membership.objects.get_or_create(society=society ,member=Student.objects.get(user=request.user))
    return HttpResponse()

#View to not attend an event
@login_required
def unattendEvent(request):
    if request.method == 'GET':
        society_slug = request.GET['society']
        society = Society.objects.get(slug = society_slug.lower())
        if society:
            Membership.objects.filter(society=society, member=Student.objects.get(user=request.user)).delete()
    return HttpResponse()

#View to allow payment for subscription in a society
@login_required
def payment(request):
    return render(request, "societly/payment.html", {})