# SJSU CMPE 138 Spring 2022 TEAM6
from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import redirect
from .sql_query import login_verify
from .sql_query.all_query import director
from .sql_query.all_query import aquarist
from .sql_query.all_query import curator
from .sql_query.all_query import event_manager


def welcome(request):
    """
    gallery page
    :param request:
    :return:
    """

    return render(request, 'Home/home.html')


def index(request):
    """
    Login page
    :param request:
    :return:
    """
    return render(request, 'Login/signin.html')


def register(request):
    """
    trgger sql query when front page submit something
    get job type,user id, user name, phone number,email and password
    return to director page if sql query succeed.
    go to login page if query failed

    show regular register page by default
    :param request:
    :return:
    """
    if request.method == "POST":
        pass
        reg_info = []
        reg_info.append(request.POST.get('selection'))
        reg_info.append(request.POST.get('u_id'))
        reg_info.append(request.POST.get("uname"))
        reg_info.append(request.POST.get("phone"))
        reg_info.append(request.POST.get("email"))
        reg_info.append(request.POST.get("pwd"))
        dire = director()
        res = dire.hire_staff(*reg_info)
        if res:
            url = reverse('main_report', kwargs = {'job_title': 'DIRECTOR', "actions": "view"})
            return redirect(url)
        else:
            return redirect('login_page')

    return render(request, 'Register/register.html')


def log_in(request):
    """
    get username and pwd from webpage,
    using query to see where it exsits.
    if exsit,redirect to relative pages.
    meanwhile store job title by finding data table,
    and store ID into session
    otherwise return default login page
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
            return render(request, 'Login/signin.html', {'msg': 'username or password wrong'})

    return render(request, 'Login/signin.html')


def report_view(request, job_title):
    """
    filer to different type of webpage based on the job title
    return signin if no job title passby
    :param request:
    :return:
    """
    if job_title == "AQUARIST" or job_title == "CURATOR" or job_title == "MANAGER" or job_title == "DIRECTOR":
        # test AQUARIST
        # username = 987153744
        # test CURATOR
        # username = 736289249
        # test MANAGER
        # username = 218363685
        # test DIRECTOR
        # username = 517465989
        url = reverse('main_report', kwargs = {'job_title': job_title, "actions": "view"})
        return redirect(url)

    return render(request, 'Login/signin.html')


def main_view(request, actions, job_title):
    """
    4 basic report pages by 4 kinds of title
    pass actions,actions for html/url tag
    DIRECTOR:
    regular:
    read assigned curator-animal, event manager-event, aquraist-facility, aquraist-event table;
    read all staff from diffeernt tables; read all event
    post:
    pass 2 date and event type to find relative events

    AQUARIST:
    regular:
    read current staff's maintain report by it's id

    CURATOR:
    regular:
    read current staff's animal report by it's id
    read exsit animas' empty facilities except restroom

    MANAGER:
    regular:
    read current staff's event report by it's id
    read all workers with counts of events that the person is working on
    read all facilities that is not hosting an event
    read all managing events and their data & Attendance
    :param request:
    :param actions:
    :param job_title:
    :return:
    """
    if actions == 'view' and job_title == 'DIRECTOR':
        dire = director()
        value = dire.view_staff_report()
        all_stf = dire.check_all_staff()
        all_eve = dire.check_all_events()
        cont = {
            'actions': actions,
            'job_title': actions,
            'animal_h': value[0],
            'animal_r': value[1],
            'manager_h': value[2],
            'manager_r': value[3],
            'aquarist_h': value[4],
            'aquarist_r': value[5],
            'event_h': value[6],
            'event_r': value[7],
            'all_staff_h': all_stf[0],
            'all_staff_r': all_stf[1],
            'all_eve_h': all_eve[0],
            'all_eve_r': all_eve[1]
        }
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        selected = request.POST.get('selection')
        event_ranges = [selected, from_date, to_date]
        if from_date and to_date and selected:
            res = dire.view_event(*event_ranges)
            cont['event_range_h'] = res[0]
            cont['event_range_r'] = res[1]
        return render(request, "Director/director.html", cont)

    elif actions == 'view' and job_title == 'AQUARIST':
        aq = aquarist()
        id = request.session['id']
        result = aq.check_maint_times(id)
        cont = {
            'actions': actions,
            'job_title': job_title,
            'aqu_h': result[0],
            'aqu_r': result[1]
        }
        return render(request, "Aquarist/aquarist.html", cont)

    elif actions == 'view' and job_title == 'CURATOR':
        cura = curator()
        result1 = cura.check_an_Status()
        result2 = cura.view_all_facilities()
        id_list = []
        for i in result1[1]:
            id_list.append(i[1])
        cont = {
            'actions': actions,
            'job_title': job_title,
            'cura_h': result1[0],
            'cura_r': result1[1],
            'ava_h': result2[0],
            'ava_r': result2[1],
        }

        return render(request, "Curator/curator.html", cont)

    elif actions == 'view' and job_title == 'MANAGER':
        mana = event_manager()
        mana_id = request.session['id']
        repo = mana.view_my_events(mana_id)
        ava_aqu = mana.check_aquarist_availability()
        ava_fac = mana.check_facility_availability()
        eve_att = mana.view_event_instances(mana_id)
        cont = {
            'actions': actions,
            'job_title': job_title,
            'repo_h': repo[0],
            'repo_r': repo[1],
            'ava_aqu_h': ava_aqu[0],
            'ava_aqu_r': ava_aqu[1],
            'ava_fac_h': ava_fac[0],
            'ava_fac_r': ava_fac[1],
            'eve_att_h': eve_att[0],
            'eve_att_r': eve_att[1],
        }
        return render(request, "Event_manager/event_manager.html", cont)


def editing(request, job_title, actions):
    """
    execute some regular action on pages from different jobs
    then return to report page(refresh)
    DIRECTOR:
    reset facility to false, animal to 0.
    Assgin all event_instance with event id and date # todo 所以后面显示不出来

    AQUARIST:
    set facility to true by facility id and time

    CURATOR:
    set animal to true by animal id

    :param request:
    :param job_title:
    :param actions:
    :return:
    """
    if actions == 'view' and job_title == 'DIRECTOR':
        dire = director()
        dire.refreshAll()
    elif actions == 'view' and job_title == 'AQUARIST':
        aq = aquarist()
        arg_list = [request.POST.get('maintain_id'), request.POST.get('maintain_time')]
        aq.maintain_facility(*arg_list)
    elif actions == 'view' and job_title == 'CURATOR':
        cur = curator()
        arg = request.POST.get('animal_id')
        if arg:
            cur.update_an_Status(arg)

    url = reverse('main_report', kwargs = {'job_title': job_title, "actions": "view"})
    return redirect(url)


def event_manager_edit(request, job_title, actions, subaction):
    """
    special edit class for manager, it has lots of modification
    return to report page when single action done
    aquarists_sign:
    assign aquarist to event by aquarist id and event id
    facility assign:
    assign facility to event by facility id and event id
    attence assign
    pass number of attend people to an event with event id
    :param request:
    :param job_title:
    :param actions:
    :param subaction:
    :return:
    """
    ev_man = event_manager()
    if subaction == 'aquarists_sign':
        aqu_id = request.POST.get('aqu_id');
        eve_id = request.POST.get('eve_id');
        ev_man.assign_aquarist_to_event(aqu_id, eve_id)
    elif subaction == 'facility_assign':
        fac_id = request.POST.get('fac_id');
        eve_id = request.POST.get('eve_id');
        ev_man.assign_facility_to_event(fac_id, eve_id)
    elif subaction == 'att_assign':
        eve_id = request.POST.get('eve_id');
        att_num = request.POST.get('att_num');
        ev_man.log_event_attendance(eve_id, att_num)

    url = reverse('main_report', kwargs = {'job_title': job_title, "actions": "view"})
    return redirect(url)


def fire(request, job_title, actions):
    id = request.POST.get('fire_delete')
    dire = director()
    res = dire.fire_staff(id)
    if res:
        print("ok")
    url = reverse('main_report', kwargs = {'job_title': job_title, "actions": "view"})
    return redirect(url)


def deleting(request, job_title, actions):
    """
    delete data from tables
    DIRECTOR:
    delete event from event table by event id
    CURATOR:
    delete relative animal with its id and animal id
    :param request:
    :param job_title:
    :param actions:
    :return:
    """
    if actions == 'view' and job_title == 'DIRECTOR':
        id = request.POST.get('event_delete')
        if len(id) == 6:
            dire = director()
            res = dire.cancel_event(id)
            # if res:
            #     print("ok")

    elif actions == 'view' and job_title == 'CURATOR':
        cur = curator()
        arg = request.POST.get('animal_id')
        if arg:
            res = cur.remove_animal(request.session['id'], arg)
            # if res:
            #     print('ok')

    url = reverse('main_report', kwargs = {'job_title': job_title, "actions": "view"})
    return redirect(url)


def creating(request, job_title, actions):
    """
    insert data into different tables
    DIRECTOR:
    create a new event by assign event id, title,type and manager id
    CURATOR:
    add a new animal under his name into table with animal id,name, type,facility id
    :param request:
    :param job_title:
    :param actions:
    :return:
    """
    if actions == 'view' and job_title == 'DIRECTOR':
        create_event = []
        create_event.append(request.POST.get('event_id'))
        create_event.append(request.POST.get('event_title'))
        create_event.append(request.POST.get('create_selection'))
        create_event.append(request.POST.get('event_overseer'))
        if create_event[0] and create_event[1] and create_event[2] and create_event[3]:
            dire = director()
            res = dire.create_event(*create_event)

    elif actions == 'view' and job_title == 'CURATOR':
        cur = curator()
        arg_list = []
        arg_list.append(request.POST.get('animal_id'))
        arg_list.append(request.POST.get('animal_name'))
        arg_list.append(request.POST.get('selection'))
        arg_list.append(request.session['id'])
        arg_list.append(request.POST.get('facility_id'))
        cur.add_new_animal(*arg_list)

    url = reverse('main_report', kwargs = {'job_title': job_title, "actions": "view"})
    return redirect(url)


def check_title(request):
    """
    by checking the database table name set the job title for it
    aquarist:AQUARIST
    curator:CURATOR
    event_manager:MANAGER
    general_manager:DIRECTOR
    """
    table = request.session['table']
    if table is not None:
        if table == "aquarist":
            request.session['title'] = 'AQUARIST'
        elif table == "curator":
            request.session['title'] = 'CURATOR'
        elif table == "event_manager":
            request.session['title'] = 'MANAGER'
        elif table == "general_manager":
            request.session['title'] = 'DIRECTOR'
