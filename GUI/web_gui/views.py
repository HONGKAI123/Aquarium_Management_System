# SJSU CMPE 138 Spring 2022 TEAM6
from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
# from django.forms.widgets import DateInput
from .sql_query import login_verify
from .sql_query.all_query import director
from .sql_query.all_query import aquarist
from .sql_query.all_query import curator


# from .sql_query.all_query import query


# ok
def welcome(request):
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
    if request.method == "POST":
        request.session['table'] = ''
        login_info = [request.POST.get('username'), request.POST.get('pwd')]
        if login_info[0] and login_info[1]:
            res = login_verify.verify_user(*login_info)
            if res[1]:
                request.session['table'] = res[0]
                request.session['id'] = login_info[0]
                check_title(request)
                url = reverse('report_pages', kwargs = {"job_title": request.session['title']})
                return redirect(url)
        else:
            print("login_post_else")
            return render(request, 'Login/signin.html', {'msg': 'username or password wrong'})

    elif request.method == "GET":
        print("login_get")
        return render(request, 'Login/signin.html')


def report_view(request, job_title):
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
            'aqu_h': result[0],
            'aqu_r': result[1]
        }
        return render(request, "Aquarist/aquarist.html", cont)

    elif job_title == "CURATOR":
        cura = curator()
        result1 = cura.check_an_Status()
        # result2 = cura.check_spare_facility(request.session.get('species'))
        # print("curator,check_spare_facility",result2)
        cont = {
            'cura_h': result1[0],
            'cura_r': result1[1],
            # 'ava_h': result2[0],
            # 'ava_r': result2[1],
        }
        return render(request, "Curator/curator.html", cont)
    elif job_title == "MANAGER":
        return render(request, "Event_manager/")
    elif job_title == "DIRECTOR":
        # test login dire
        # username = 517465989
        # password = 517465989
        url = reverse('main_report', kwargs = {'job_title': job_title, "actions": "view"})
        return redirect(url)

    return render(request, 'Login/signin.html')


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


def main_view(request, actions, job_title):
    if actions == 'view' and job_title == 'DIRECTOR':
        dire = director()
        value = dire.view_staff_report()
        cont = {
            'actions': actions,
            'job_title': job_title,
            'animal_h': value[0],
            'animal_r': value[1],
            'manager_h': value[2],
            'manager_r': value[3],
            'aquarist_h': value[4],
            'aquarist_r': value[5],
            'event_h': value[6],
            'event_r': value[7],
        }
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        selected = request.POST.get('selection')
        event_ranges = [selected, from_date, to_date]
        if from_date and to_date and selected:
            # print("dire.date", from_date, to_date)
            res = dire.view_event(*event_ranges)
            # print("res", res)
            cont['event_range_h'] = res[0]
            cont['event_range_r'] = res[1]
        return render(request, "Director/director.html", cont)


def editing(request):
    pass


def deleting(request, job_title, actions):
    print(request.POST.get('event_delete'))
    if actions == 'view' and job_title == 'DIRECTOR':
        id = request.POST.get('event_delete')
        if len(id) == 6:
            dire = director()
            res = dire.cancel_event(101001)
            if res:
                print("ok")
        url = reverse('main_report', kwargs = {'job_title': job_title, "actions": "view"})
        return redirect(url)
    pass


def creating(request, job_title, actions):
    print(request.POST.get('event_create'))
    if actions == 'view' and job_title == 'DIRECTOR':
        create_event = []
        create_event.append(request.POST.get('event_id'))
        create_event.append(request.POST.get('event_title'))
        create_event.append(request.POST.get('create_selection'))
        create_event.append(request.POST.get('event_overseer'))
        if create_event[0] and create_event[1] and create_event[2] and create_event[3]:
            dire = director()
            res = dire.create_event(*create_event)
            if res:
                print("ok")
        url = reverse('main_report', kwargs = {'job_title': job_title, "actions": "view"})
        return redirect(url)
    pass


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
        print(reg_info, "\t", *res)
    url = reverse('signup')
    return redirect(url)
    return render(request, 'Register/register.html')
