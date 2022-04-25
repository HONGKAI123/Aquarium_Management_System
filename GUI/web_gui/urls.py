from django.urls import path
from . import views

urlpatterns = [
    #path('index/',views.index),
    path('',views.index),
    path('',views.index,name = 'login')
]
