from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Student(models.Model):

    matricNo = models.CharField(max_length = 10, unique = True, primary_key = True)
    username = models.CharField(max_length = 30, unique = True)
    password = models.CharField(max_length = 256)
    picture = models.ImageField(blank = True)
    email = models.EmailField()
    firstname = models.CharField(max_length = 30)
    lastname = models.CharField(max_length = 30)
    degree = models.CharField(max_length = 50)

    def __str__(self):
        return self.firstname + " " + self.lastname


class Society(models.Model):

    name = models.CharField(max_length = 30, unique = True)
    description = models.TextField(max_length = 2000)
    logo = models.ImageField(blank = True)
    email = models.EmailField()
    facebook = models.URLField()
    linkedin = models.URLField()
    instagram = models.URLField()
    twitter = models.URLField()
    members = models.ManyToManyField(Student, through = 'Membership')

    def __str__(self):
        return self.name


class Event(models.Model):

    name = models.CharField(max_length = 50)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField(max_length = 2000)
    image = models.ImageField(blank = True)
    organized_by = models.ManyToManyField(Society, related_name = "organized_by")
    attended_by = models.ManyToManyField(Student, related_name = "attended_by")

    def __str__(self):
        return self.name


class Review(models.Model):

    rating = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(10)
    ])
    description = models.CharField(max_length = 2000)
    event = models.ForeignKey(Event, on_delete = models.CASCADE, related_name = "eventReviews")
    made_by = models.ForeignKey(Student, on_delete = models.CASCADE, related_name = "reviewed_by")

    def __str__(self):
        return self.rating


class Membership(models.Model):

    ROLE = (
        ('1', 'Member'),
        ('2', 'Board Member')
    )

    member = models.ForeignKey(Student, on_delete = models.CASCADE)
    society = models.ForeignKey(Society, on_delete = models.CASCADE)
    date_joined = models.DateField(auto_now = True)
    is_board = models.CharField(choices = ROLE, default = '2', max_length = 1)