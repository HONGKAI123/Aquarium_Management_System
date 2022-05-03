# SJSU CMPE 138 Spring 2022 TEAM6
from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import redirect
from .sql_query import login_verify
from .sql_query.all_query import director

# from .sql_query.all_query import query

from django.http import HttpResponse


def welcome(request):
    """
    test pages, check sql connection
    """
    # event test ok
    # temp = director.view_event('exhibit', '2022-05-02', '2022-05-04')
    # print(temp)
    # test_data = [('101001', 'penguin exhibit', 'exhibit', datetime.date(2022, 5, 4), 130), ('101001', 'penguin exhibit', 'exhibit', datetime.date(2022, 5, 3), 120), ('101002', 'whale exhibit', 'exhibit', datetime.date(2022, 5, 4), 100)]
    # test_data_header = ['id','name','type','date','attendence']
    # return render(request,'Director1/director.html',{"job_title":"fuck!","main_table":test_data,"main_table_header":test_data_header,'page_title':'YO bitch'})


def index(request):
    return render(request, 'Login/signin.html')

def log_in(request):
    """
    get username and pwd from webpage,
    using query to see where it exsits.
    if exsit,redirect to relative pages,
    otherwise return error
    """
    # test login
    # username = 517465989
    # password = 517465989
    if request.method == "POST":
        request.session['table'] = ''
        login_info = [request.POST.get('username'),request.POST.get('pwd')]
        if login_info[0] and login_info[1]:
            res = login_verify.verify_user(*login_info)
            if res[1]:
                request.session['table'] = res[0]
                check_title(request)
                url = reverse('jobs_page',kwargs = {"job_title":request.session['title']})
                return redirect(url)
            else:
                return render(request, 'Login/signin.html', {'msg': 'username or password wrong'})

    elif request.method == "GET":
        return render(request, 'Login/signin.html')


def report(request,job_title):
    """
    return different type of webpage based on the job title
    :param request:
    :return:
    """
    title = check_title(request)
    if title is not None:
        if title == 1:
            pass
        elif title == 2:
            pass
        elif title == 3:
            pass
        elif title == 4:
            dire = director()
            value = dire.view_staff_report()
            print(value)
            cont = {
                'animal_h':value[0],
                'animal_r':value[1],
                'manager_h':value[2],
                'manager_r':value[3],
                'aquarist_h':value[4],
                'aquarist_r':value[5],
                'event_h':value[6],
                'event_r':value[7]
            }
            return render(request, 'Director/director.html',cont)
    else:
        return render()


"""
:return 0 if the session/cookie value invalid
by checking the table name set the job title for it
title = staff, when table is aquarist,curator,event_manager
title = Director1 when table is general_manager
return 1 for aquarist
return 2 for curator
return 3 for event_manager
return 4 for general_manager
"""
def check_title(request) -> int:
    table = request.session['table']
    if table is not None:
        if table == "aquarist":
            request.session['title'] = 'staff'
            return 1
        elif table == "curator":
            request.session['title'] = 'staff'
            return 2
        elif table == "event_manager":
            request.session['title'] = 'staff'
            return 3
        elif table == "general_manager":
            request.session['title'] = 'DIRECTOR'
            return 4
    else:
        return 0


def dire(request):
    return render(request, "Director/director.html")

def home(request):
    return render(request, 'Home/Home.html')

def register(request):
    return render(request, 'Register/register.html')
