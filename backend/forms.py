from django import forms
from .models import Student, Society, Event, Review, Membership
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username','email','password')

class LogInForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:

		model = User
		fields = ('username','password')


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('matricNo', 'picture', 'year', 'degree')

class SocietyForm(forms.ModelForm):

    name = forms.CharField(max_length = 128, help_text = "Please enter the name of the society")
    description = forms.CharField(widget = forms.Textarea)
    email = forms.EmailField(widget = forms.EmailInput)
    facebook = forms.URLField(widget = forms.URLInput)
    twitter = forms.URLField(widget = forms.URLInput)
    linkedin = forms.URLField(widget = forms.URLInput)
    instagram = forms.URLField(widget = forms.URLInput)

    class Meta:

        model = Society
        exclude = ('members',)


class EventForm(forms.ModelForm):

    name = forms.CharField(max_length = 128, help_text = "Please enter the name of the event")
    date = forms.CharField(widget = forms.DateInput)
    time = forms.CharField(widget = forms.TimeInput)
    description = forms.CharField(widget = forms.Textarea)
    image = forms.ImageField()

    class Meta:

        model = Event
        exclude = ('attended_by', 'organized_by',)


class ReviewForm(forms.ModelForm):

    rating = forms.IntegerField(max_value = 10, min_value = 0)
    description = forms.CharField(widget = forms.Textarea)

    class Meta:
        model = Review
        exclude = ('event', 'made_by')



class MemberForm(forms.ModelForm):

    YEAR = (
        ('1', 'Freshman'),
        ('2', 'Sophomore'),
        ('3', 'Junior'),
        ('4', 'Senior'),
        ('5', 'Postgraduate')
    )

    matricNo = forms.CharField(max_length = 10)
    picture = forms.ImageField()
    year = forms.ChoiceField(choices = YEAR, widget = forms.RadioSelect)
    degree = forms.CharField(max_length = 50)

    class Meta:

        model = Student
        fields = ('matricNo', 'picture', 'year', 'degree',)
