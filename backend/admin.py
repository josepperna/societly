from django.contrib import admin
from .models import Student, Society, Event, Review, Membership

# Register your models here.
admin.site.register(Student)
admin.site.register(Society)
admin.site.register(Event)
admin.site.register(Review)
admin.site.register(Membership)