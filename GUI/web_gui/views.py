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
    return render(request, 'Home/home.html')


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
        login_info = [request.POST.get('username'), request.POST.get('pwd')]
        if login_info[0] and login_info[1]:
            res = login_verify.verify_user(*login_info)
            if res[1]:
                request.session['table'] = res[0]
                request.session['id'] = login_info[0]
                check_title(request)
                url = reverse('jobs_page', kwargs = {"job_title": request.session['title']})
                return redirect(url)

        else:
            print("else")
            return render(request, 'Login/signin.html', {'msg': 'username or password wrong'})

    elif request.method == "GET":
        return render(request, 'Login/signin.html')


def report(request, job_title):
    """
    return different type of webpage based on the job title
    :param request:
    :return:
    """
    title = check_title(request)

    if job_title == "AQUARIST":
        # sample 987153744
        aq = aquarist()
        id = request.session['id']
        result = aq.check_maint_times(id)
        print(result)
        cont = {
            'aqu_h': result[0],
            'aqu_r': result[1]
        }
        return render(request, "Aquarist/aquarist.html", cont)

    elif job_title == "CURATOR":
        # sample 705628448
        cura = curator()
        result1 = cura.check_an_Status()
        #result2 = cura.check_spare_facility(request.session.get('species'))
        cont = {
            'cura_h': result1[0],
            'cura_r': result1[1],
            # 'ava_h': result2[0],
            # 'ava_r': result2[1],
        }
        return render(request, "Curator/curator.html", cont)
        # return render(request, "")
    elif job_title == "MANAGER":
        # sample 218363685
        # todo
        return render(request, "Event_manager/")
    elif job_title == "DIRECTOR":
        event_list = []
        print(request.POST.get('from_date'))
        event_list.append(request.POST.get('selection'))
        print(event_list)
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
        print("job_title",job_title)
        return render(request, 'Login/signin.html')

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
    if request.method == "POST":
        pass
        reg_info = []
        reg_info.append(request.POST.get('selection'))
        reg_info.append(request.POST.get("uname"))
        reg_info.append(request.POST.get("email"))
        reg_info.append(request.POST.get("phone"))
        reg_info.append(request.POST.get("pwd"))

        dire = director()
        res = dire.hire_staff(*reg_info)
        print(reg_info,"\t",*res)
    # url = reverse('signup')
    # return redirect(url)
    return render(request, 'Register/register.html')
