from django.conf.urls import url
from backend import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.index, name='login'),
    url(r'^about-us/', views.about_us, name='about-us'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^userlogin/',views.log_in_form,name = 'login'),
    url(r'^contact-us/', views.contact_us, name='contact_us'),
    url(r'^register/', views.register, name='register'),
    url(r'^faq/', views.faq, name='faq'),
    url(r'^society/(?P<society_name_slug>[\w\-]+)/$', views.society, name='society'),
<<<<<<< HEAD
    url(r'^showallsoc/$', views.show_all_societies, name='logout'),
    url(r'^showalleve/$', views.show_all_events, name='logout'),
    url(r'^showallmysoc/$', views.show_your_societies, name='logout'),
    url(r'^showallmyeve/$', views.show_your_events, name='logout'),
=======
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^society/', views.societies, name='societies'),
>>>>>>> feca76de4ea04a5713f4022d9d1bdd512028c998
]
