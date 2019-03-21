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
def index(request):
    if request.user and request.user.is_authenticated:
        return profile(request)
    else:
        return render(request, "societly/home.html")

def show_all_societies(request):
    societies = Society.object.order_by('date')
    context_dict = {'societies': societies}
    return render(request, 'societly/Show_all_societies.html', context_dict)

@login_required
def show_your_societies(request):
    student = Student.objects.filter(user = request.user)
    societies = student.society_set.all()
    context_dict = {'societies': societies}
    print(societies)
    return render(request, 'societly/Show_all_societies.html', context_dict)

def show_all_events(request):
    events = Event.object.order_by('date')
    context_dict = {'events': events}
    return render(request, 'societly/Show_all_events.html', context_dict)


@login_required
def show_your_events(request):
    student = Student.objects.filter(user = request.user)
    events = student.event_set.all()
    context_dict = {'events': events}
    print(events)
    return render(request, 'societly/Show_all_events.html', context_dict)


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
                print("yes")
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
        context_dict['societies'] =  Membership.objects.filter(member = member).order_by('-date_joined')[:3]
        print(context_dict['societies'])
        # context_dict['memberships'] = len(list(memberships))
        context_dict['events'] = Event.objects.filter(attended_by = member).order_by('-date')[:3]
        print(context_dict['events'])
        # context_dict['societies'] = None
        context_dict['memberships'] = None
        # context_dict['events'] = None
        context_dict['picture'] = member.picture
    except Exception as e: 
        print(e)

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

def contact_us(request):
    return render(request, "societly/contact-us.html")

def faq(request):
    return render(request, "societly/faq.html")

def societies(request):
    return render(request, "societly/Show_all_societies.html")

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

def society(request, society_name_slug):
    context_dict = {}
    try:
        society = Society.objects.filter(slug = society_name_slug).first()
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
        context_dict['society'] = None
        context_dict['events'] = None
        context_dict['member'] = False
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

@login_required
def add_event(request, society_slug_name):
    if request.method == 'POST':
        event_form = EventForm(data = request.data)
        society = Society.objects.filter(slug = society_slug_name).first()
        student = Student.objects.filter(user = request.user).first()
        membership = society.membership_set.filter(society = society, member = student)
        
        if event_form.is_valid() and membership.is_board == '2':
            ev = event_form.save()
            ev.organized_by = society

            if 'image' in request.FILES:
                print("yes")
                ev.image = request.FILES['image']

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

@login_required 
def user_logout(request): 
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def subscribe_to_society(request):
    if request.method == 'GET':
        society_slug = request.GET['society']
        society = Society.objects.get(slug = society_slug)
        if society:
            Membership.objects.get_or_create(society=society ,member=Student.objects.get(user=request.user))
    return HttpResponse()

@login_required
def unsubscribe_from_society(request):
    if request.method == 'GET':
        society_slug = request.GET['society']
        society = Society.objects.get(slug = society_slug)
        if society:
            Membership.objects.filter(society=society, member=Student.objects.get(user=request.user)).delete()
    return HttpResponse()