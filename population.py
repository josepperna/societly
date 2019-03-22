import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'societly.settings')

from django.core.files import File
import django
django.setup()
from backend.models import Student, Society, Event, Membership
from django.contrib.auth.models import User
from datetime import date, datetime
def populate():
    users = [
        {"username": "societly",
        "email": "societly@gmail.com",
        "password": "admin123789"},
        {"username": "glasgow",
        "email": "glasgow@gmail.com",
        "password": "admin789123"},
    ]
    students = [
        {"user" : "aeiou",
        "matricNo" : "2221111A",
        "degree" : "Computing",
        "year" : 5},
        {"user" : "tsdfna",
        "matricNo" : "2221133A",
        "degree" : "Maths",
        "year" : 1},
        ]
    societies = [
        {"name" : "GUSC",
        "description" : "A very interesting society",
        "email" : "aslfa@gmail.com",
        "linkedin" : "www.linked.in"},
        {"name" : "GU Trading Society",
        "description" : "Description is the pattern of narrative development that aims to make vivid a place, object, character, or group. Description is one of four rhetorical modes, along with exposition, argumentation, and narration. In practice it would be difficult to write literature that drew on just one of the four basic modes.",
        "email" : "asdnfn@gmail.com",
        "linkedin" : "www.linked.in"},
    ]
    events = [
        {"name" : "Dinner",
        "description" : "A very interesting event",},
        {"name" : "Lunch",
        "description" : "Description is the pattern of narrative development that aims to make vivid a place, object, character, or group. Description is one of four rhetorical modes, along with exposition, argumentation, and narration. In practice it would be difficult to write literature that drew on just one of the four basic modes.",},
    ]


    for i in range(2):
        u = add_user(users[i]["username"], users[i]["email"], users[i]["password"])
        student = add_student(students[i]["matricNo"], u, students[i]["degree"], students[i]["year"])
        s = add_society(societies[i]["name"], societies[i]["description"], societies[i]["email"], societies[i]["linkedin"])
        add_event(events[i]["name"], events[i]["description"], s, student)
        add_membership(student, s, i+1)
        

def add_user(username, email, password):
    u = User.objects.create_user(username=username, email=email, password=password)
    u.save()
    return u

def add_society(name, desc, email, linkedin):
    s = Society.objects.get_or_create(name=name)[0]
    s.description = desc
    s.email = email
    s.linkedin = linkedin
    s.logo.save('abc.jpg', File(open('aaa.jpg', 'rb')))
    s.save()
    return s

def add_event(name, desc, society, student):
    e = Event.objects.get_or_create(name=name)[0]
    e.description = desc
    e.organized_by.set([society])
    e.attended_by.set([student])
    e.image.save('abc.jpg', File(open('aaa.jpg', 'rb')))
    e.save()
    return e

def add_student(matricNo, user, degree, year):
    s = Student.objects.get_or_create(matricNo=matricNo)[0]
    s.picture.save('abc.jpg', File(open('aaa.jpg', 'rb')))
    s.user = user
    s.save()
    return s

def add_membership(member, society, isBoard):
    m = Membership.objects.get_or_create(member=member, society=society)[0]
    m.is_board = str(isBoard)
    m.save
    return m

if __name__ == '__main__':
    print("Starting Rango population script...") 
    populate()