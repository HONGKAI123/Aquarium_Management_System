from django.urls import path
from . import views

urlpatterns = [
    #path('index/',views.index),
    path('',views.welcome),
    path('login/',views.log_in,name = 'login'),
    path('director/',views.dire,name = 'dire_edit')
]
