from django.shortcuts import render
from .sql_query import login_verify

# from .sql_query.all_query import query

from django.http import HttpResponse


def welcome(request):
    """
    test pages, check sql connection
    """
    # from .sql_query import sql_connection
    # conn = sql_connection.connector()
    # conn = conn.connect()
    from .sql_query import all_query
    aqu = all_query.aquarist()
    # res = aqu.check_maint_times('987153744')
    # print(res[0])
    # print(res[1])

    # q = all_query.query()
    # cur = q.cursor()
    arg = ['987153744', '300001', '12:00:00']
    # cur.execute("UPDATE facility_maint \
    #     SET maint_status = true \
    #     WHERE facility = '" + arg[1] + "' \
    #     AND maint_time = '" + arg[2] + "';")
    # res = cur.fetchall()
    # q.conn.commit()
    # print(cur.rowcount)
    # q.disconnect()
    # print(res)

    res = aqu.maintain_facility(*arg)
    print(res)
    return render(request, 'index.html')

    with connection.cursor() as cursor:
        cursor.execute(r"SELECT * FROM animal")
        row = cursor.fetchall()
    print(row)

    # event test ok
    # temp = director.view_event('exhibit', '2022-05-02', '2022-05-04')
    # print(temp)
    # test_data = [('101001', 'penguin exhibit', 'exhibit', datetime.date(2022, 5, 4), 130), ('101001', 'penguin exhibit', 'exhibit', datetime.date(2022, 5, 3), 120), ('101002', 'whale exhibit', 'exhibit', datetime.date(2022, 5, 4), 100)]
    # test_data_header = ['id','name','type','date','attendence']
    # return render(request,'Director/director.html',{"job_title":"fuck!","main_table":test_data,"main_table_header":test_data_header,'page_title':'YO bitch'})


def index(request):
    return render(request, 'Login/signup.html')


def log_in(request):
    """
    get username and pwd from webpage,
    using query to see where it exsits.
    if exsit,redirect to relative pages,
    otherwise return error
    """
    if request.method == "POST":
        # todo
        # todo miss select user from each table
        # todo by get user from different table, show the different webpage to them
        # todo set session about the title
        request.session['table'] = ''

        login_info = []
        login_info.append(request.POST.get('username'))
        login_info.append(request.POST.get('pwd'))
        if login_info[0] and login_info[1]:
            res = login_verify.verify_user(*login_info)
            if res[1]:
                request.session['table'] = res[0]
                return render(request, 'Director/director.html', {'job_title':request.session['table'] })
            else:
                return render(request, 'Login/signup.html', {'msg': 'username or password wrong'})

    elif request.method == "GET":
        return render(request, 'Login/signup.html')


def report(request):
    """
    return different type of webpage based on the job title
    :param request:
    :return:
    """
    title = check_title(request)
    if title > 0:
        if title == 1:
            pass
            # todo sql query
            return render(request, 'Director/director.html', {'table_value'})
        elif title == 2:
            pass
        elif title == 3:
            pass
        elif title == 4:
            pass
    else:
        return render()


"""
:return 0 if the session/cookie value invalid
by checking the table name set the job title for it
title = staff, when table is aquarist,curator,event_manager
title = Director when table is general_manager
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
            request.session['title'] = 'Director'
            return 4
    else:
        return 0


def dire(request):
    pass
