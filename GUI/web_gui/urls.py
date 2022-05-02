# SJSU CMPE 138 Spring 2022 TEAM6
from django.urls import path
from . import views

urlpatterns = [
    #path('index/',views.index),
    path('',views.welcome),
    path('login/',views.log_in,name = 'login'),
    path('director/',views.dire,name = 'dire_edit'),
    path('Home',views.home, name='home'),
    path('register',views.register, name='tiny')
]
