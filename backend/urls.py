from django.conf.urls import url
from backend import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'society/', views.society_page, name='society_page')
]

