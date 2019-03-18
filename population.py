import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'societly.settings')

import django
django.setup()
from backend.models import Student, Society

def populate():
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
        "description" : "A very interesting society",
        "email" : "asdnfn@gmail.com",
        "linkedin" : "www.linked.in"},
    ]

    for student in students:
        add_student(student["matricNo"], student["user"], student["degree"], student["year"])

    for society in societies:
        add_society(society["name"], society["description"], society["email"], society["linkedin"])

def add_society(name, desc, email, linkedin):
    s = Society.objects.get_or_create(name=name)[0]
    print("aaaa")
    s.description = desc
    s.email = email
    s.linkedin = linkedin
    s.save()
    return s

def add_student(matricNo, user, degree, year):
    s = Student.objects.get_or_create(matricNo=matricNo)[0]
    #s.user = user
    s.save()
    return s

if __name__ == '__main__':
    print("Starting Rango population script...") 
    populate()