# SJSU CMPE 138 Spring 2022 TEAM4
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.welcome),
    path(r'login/', views.log_in, name = 'login_page'),
    re_path(r'register/', views.register, name = 'reg'),
    re_path(r'^(?P<job_title>\w+)/$', views.report_view, name = 'report_pages'),
    re_path(r'^(?P<job_title>\w+)/(?P<actions>\w+)/$', views.main_view, name = 'main_report'),
    re_path(r'^(?P<job_title>\w+)/(?P<actions>\w+)/edit/$', views.editing, name = 'jobs_edit'),
    re_path(r'^(?P<job_title>\w+)/(?P<actions>\w+)/delete/$', views.deleting, name = 'jobs_delete'),
    re_path(r'^(?P<job_title>\w+)/(?P<actions>\w+)/create/$', views.creating, name = 'jobs_create'),



    # path('DIRECTOR/view/new',views.dire_view,name = 'dire_new'),

    # re_path(r'^(?P<job_title>\w+)/(?P<actions>\w+)/$', views.report, name = 'search'),

    # re_path(r'^(?P<job_title>\w+)/(?P<review>\w+)/$', views.dire, name = 'jobs_page'),
    # path('search/', views.dire, name = 'search'),
    re_path(r'signup/', views.register, name = "signup")
    # re_path(r'^(?P<title>\w+)/(?P<op>\w+)/$',views.todo_view,name='ops'),

    # path('',views.welcome),
    # path('login/',views.log_in,name = 'login'),
    # path('director/',views.dire,name = 'dire_edit'),
    # path('Home',views.home, name='home'),
    # path('register',views.register, name='tiny')
]
