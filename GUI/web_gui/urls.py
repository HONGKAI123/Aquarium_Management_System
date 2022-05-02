from django.urls import path,re_path
from . import views

urlpatterns = [
    #path('index/',views.index),
    # path('',views.welcome),
    path('',views.log_in,name = 'login'),
    path(r'login/',views.log_in,name = 'login'),
    re_path(r'^(?P<title>\w+)/$',views.report,name = 'jobs'),
    re_path(r'^(?P<title>\w+)/(?P<op>\w+)/$',views.todo_view,name='ops'),
]
