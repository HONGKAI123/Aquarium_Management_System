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
    re_path(r'^(?P<job_title>\w+)/(?P<actions>\w+)/edit/(?P<subaction>\w+)$', views.event_manager_edit,
            name = 'manage_edit'),
    re_path(r'^(?P<job_title>\w+)/(?P<actions>\w+)/delete/$', views.deleting, name = 'jobs_delete'),
    re_path(r'^(?P<job_title>\w+)/(?P<actions>\w+)/create/$', views.creating, name = 'jobs_create'),
    re_path(r'^(?P<job_title>\w+)/(?P<actions>\w+)/delete/fire$', views.fire, name = 'jobs_fire'),
]
