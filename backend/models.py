from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.defaultfilters import slugify

# Create your models here.

	
	
class Student(models.Model):

    YEAR = (
        ('1', 'Freshman'),
        ('2', 'Sophomore'),
        ('3', 'Junior'),
        ('4', 'Senior'),
        ('5', 'Postgraduate')
    )


    user = models.OneToOneField(User, null=True)
    matricNo = models.CharField(max_length = 10, unique = True, primary_key = True)
    picture = models.ImageField(blank = True)
    degree = models.CharField(max_length = 50)
    year = models.CharField(choices = YEAR, default = '1', max_length = 1)

    class Meta:

        verbose_name = "student"
        verbose_name_plural = "students"

    def get_username(self):
        return self.user.username
    
    def get_email(self):
        return self.user.email

    def get_fullname(self, user):
        return user.first_name + " " + user.last_name

    def __str__(self):
        return self.matricNo


class Society(models.Model):

    name = models.CharField(max_length = 128, unique = True)
    description = models.TextField(max_length = 2000)
    logo = models.ImageField(blank = True)
    email = models.EmailField()
    facebook = models.URLField(blank = True)
    linkedin = models.URLField(blank = True)
    instagram = models.URLField(blank = True)
    twitter = models.URLField(blank = True)
    members = models.ManyToManyField(Student, through = 'Membership', related_name="matricNo_members_society")
    slug = models.SlugField(blank = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Society, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "society"
        verbose_name_plural = "societies"

    def __str__(self):
        return self.name


class Event(models.Model):

    name = models.CharField(max_length = 128)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField(max_length = 2000)
    image = models.ImageField(blank = True)
    organized_by = models.ManyToManyField(Society, related_name = "organized_by")
    attended_by = models.ManyToManyField(Student, related_name = "attended_by", blank = True)

    class Meta:

        verbose_name = "event"
        verbose_name_plural = "events"

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

    class Meta:

        verbose_name = "review"
        verbose_name_plural = "reviews"

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

    def __str__(self):
        return "{} {}".format(self.member, self.society)

    
