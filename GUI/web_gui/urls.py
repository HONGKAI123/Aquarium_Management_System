from django.urls import path
from . import views

urlpatterns = [
    #path('index/',views.index),
    path('',views.index),
    path('login/',views.log_in,name = 'login')
]
