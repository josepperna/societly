from django import forms
from .models import Student, Society, Event, Review, Membership
from django.contrib.auth.models import User

#Form to fill in User information
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username','email','password', 'first_name', 'last_name')

#Form for logging into the website
class LogInForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:

		model = User
		fields = ('username','password')

<<<<<<< HEAD
#Form to fill in Student information
=======
class RegisterSocietyForm(forms.ModelForm):
	class Meta:

		model = Society
		fields = ('name','description','logo','email','facebook','linkedin','instagram','twitter','members')

>>>>>>> e9707936bc89f3cf4b94f051f5a72ec406e75e1e
class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('matricNo', 'picture', 'year', 'degree')

#Form to fill in Society information
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

#Form to fill in Event information
class EventForm(forms.ModelForm):

    name = forms.CharField(max_length = 128, help_text = "Please enter the name of the event")
    date = forms.CharField(widget = forms.DateInput)
    time = forms.CharField(widget = forms.TimeInput)
    description = forms.CharField(widget = forms.Textarea)

    class Meta:

        model = Event
        exclude = ('attended_by', 'organized_by',)

#Form to fill in Review information (not implemented)
class ReviewForm(forms.ModelForm):

    rating = forms.IntegerField(max_value = 10, min_value = 0)
    description = forms.CharField(widget = forms.Textarea)

    class Meta:
        model = Review
        exclude = ('event', 'made_by')


#Form to fill in Membership information
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
