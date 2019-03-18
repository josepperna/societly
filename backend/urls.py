from django.conf.urls import url
from backend import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'about-us/', views.about_us, name='about-us'),
    url(r'<str:matricNo>/', views.profile_page, name='profile-page')
]

