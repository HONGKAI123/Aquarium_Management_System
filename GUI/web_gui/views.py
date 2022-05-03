# SJSU CMPE 138 Spring 2022 TEAM6
from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import redirect
from .sql_query import login_verify
from .sql_query.all_query import director
from .sql_query.all_query import aquarist
from .sql_query.all_query import curator

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
    print("ok")
    if request.method == "POST":
        request.session['table'] = ''
        login_info = [request.POST.get('username'), request.POST.get('pwd')]
        print(login_info)
        if login_info[0] and login_info[1]:
            res = login_verify.verify_user(*login_info)
            print(res)
            if res[1]:
                request.session['table'] = res[0]
                request.session['id'] = login_info[0]
                check_title(request)
                url = reverse('jobs_page', kwargs = {"job_title": request.session['title']})
                return redirect(url)
                # if request.session['table'] == "aquarist":
                #     url = reverse('jobs_page', kwargs = {"job_title": request.session['title']})
                #     return redirect(url)
                # elif request.session['table'] == "curator":
                #     pass
                # elif request.session['table'] == "event_manager":
                #     pass
                # elif request.session['table'] == "general_manager":
                #     url = reverse('jobs_page', kwargs = {"job_title": request.session['title']})
                #     return redirect(url)

        else:
            print("else")
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

    if job_title == "AQUARIST":
        aq = aquarist()
        id = request.session['id']
        result = aq.check_maint_times(id)
        print(result)
        cont = {
            'aqu_h':result[0],
            'aqu_r':result[1]
        }
        return render(request,"Aquarist/aquarist.html",cont)

    elif job_title == "CURATOR":
        cura = curator()
        result1 = cura.check_an_Status()
        result2 = cura.check_spare_facility(request.session.get('species'))
        cont ={
            'cura_h':result1[0],
            'cura_r':result1[1],
            'ava_h':result2[0],
            'ava_r':result2[1],
        }
        return render(request,"Curator/curator.html",cont)
        # return render(request, "")
    elif job_title == "MANAGER":
        return render(request,"Event_manager/")
    elif job_title == "DIRECTOR":
        dire = director()
        value = dire.view_staff_report()
        print(value)
        cont = {
            'animal_h': value[0],
            'animal_r': value[1],
            'manager_h': value[2],
            'manager_r': value[3],
            'aquarist_h': value[4],
            'aquarist_r': value[5],
            'event_h': value[6],
            'event_r': value[7]
        }
        # todo edit/delete 缺 id
        return render(request, 'Director/director.html', cont)
    else:
        return render(request,'Login/signin/html')

    if request.method == "GET":
        return render(request, 'Director/director.html')


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
            request.session['title'] = 'AQUARIST'
            return 1
        elif table == "curator":
            request.session['title'] = 'CURATOR'
            return 2
        elif table == "event_manager":
            request.session['title'] = 'MANAGER'
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
