from django.conf.urls import url
from backend import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.index, name='login'),
    url(r'^about-us/', views.about_us, name='about-us'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^userlogin/',views.log_in_form,name = 'logInForm'),
    url(r'^contact-us/', views.contact_us, name='contact_us'),
    url(r'^register/', views.register, name='register'),
    url(r'^faq/', views.faq, name='faq'),
    #url(r'events/', views.profile, name='events')

   
    url(r'<str:matricNo>/', views.profile_page, name='profile-page')
]

