
from django.conf.urls import url
from app02 import views
urlpatterns = [
    url(r'^login/', views.login),
    url(r'^index/', views.index),
    url(r'^menu/', views.menu),
    ]
