from django.conf.urls import url
from backend import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login', views.index, name='login'),
    url(r'about-us/', views.about_us, name='about-us'),
    url(r'profile/', views.profile, name='profile'),
    url(r'userlogin/',views.log_in_form,name = 'logInForm'),
]

