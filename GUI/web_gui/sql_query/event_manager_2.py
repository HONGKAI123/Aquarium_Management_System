# SJSU CMPE 138 Spring 2022 TEAM6

# *arg
import mysql.connector
#from all_query import query

database = mysql.connector.connect(
    host='localhost',
    user='aq_admin',
    password='aq_Password01!',
    database='aquarium'
)

cursor = database.cursor()

def view_my_events(*args):
    """
    input: manager ID,
    return all of the event manager's events. 
    """
    sql_query = "SELECT * FROM event WHERE overseer = " + "'" + args[0] + "'"
    cursor.execute(sql_query)
    result = cursor.fetchall()
    # print(result)
    return ['ev_ID', 'title', 'type', 'facility', 'overseer'], result


def check_aquarist_availability():
    """
    list all workers with counts of events that the person is working on
    """
    # list all people, count events..
    sql_query = "SELECT staff, COUNT(*) event_count " \
                "FROM work_on " \
                "GROUP BY staff " \
                "ORDER BY COUNT(*) DESC"
    cursor.execute(sql_query)
    result = cursor.fetchall()
    # print(result)
    return ['staff', 'event_count'], result


def assign_aquarist_to_event(*args):
    """
    assign aquarist(id) to event(id) 
    """
    
    aquarist_ID = args[0]
    event_ID = args[1]
    sql_query = "INSERT INTO work_on VALUES (" + "'" + event_ID + "','" + aquarist_ID + "')"
    try:
        cursor.execute(sql_query)
        database.commit()
        print('aquarist assigned successfully')
    except:
        print('failed to assign aquarist')
    count = cursor.rowcount
    return True if count > 0 else False


def check_facility_availability():
    """
    list all facilities that is not hosting an event
    """
    sql_query = "SELECT * from facility WHERE fa_ID NOT IN (SELECT facility from event)"
    cursor.execute(sql_query)
    result = cursor.fetchall()
    return ['fa_ID', 'name'], result


def assign_facility_to_event(*args):
    """
    assign facility(id) to event(id) 
    """
    event_ID = args[0]
    facility_ID = args[1]
    sql_query = "UPDATE event SET facility = " + "'" + facility_ID + "' " + \
                "WHERE ev_ID =" + "'" + event_ID + "'"
    try:
        cursor.execute(sql_query)
        database.commit()
        print('facility assigned successfully')
    except:
        print('failed to assign facility')
    count = cursor.rowcount
    return True if count > 0 else False


def log_event_attendance(*args):
    """
    Input: recorded_attendance, event_ID
    Update an event's attendance number to an Event_instance.
    """
    event_ID = args[0]
    recorded_attendance = args[1]
    sql_query = "UPDATE event_instance SET attendance = " + str(recorded_attendance) + \
                " WHERE event = " + "'" + event_ID + "'"
    try:
        cursor.execute(sql_query)
        database.commit()
        print('event log updated successfully')
    except:
        print('failed to update event log')
    count = cursor.rowcount
    return True if count > 0 else False

def view_event_table(*args):
    """
    args = [st_ID]
    returns rows of events that the current user oversees,
    how many aquarists work on each event, 
    and which facility hosts each event
    """
    # db connection API
    #q = query()

    # build sql query
    sql_query = "\
        SELECT ev_ID, COUNT(staff), facility \
        FROM event \
        LEFT JOIN work_on ON event.ev_ID = work_on.event \
        WHERE overseer = {0} \
        GROUP BY ev_ID;".format(args[0])

    """
    # connect database
    with q.cursor(username = 'aq_admin', pwd = 'aq_Password01!') as cur:
        cur.execute(sql_query)

        res = cur.fetchall()
    """
    cursor.execute(sql_query)
    res = cursor.fetchall()
    return ['Event ID', 'Worker Count', 'Facility'], res

def view_event_instances(*args):
    """
    args = [st_ID]
    returns rows of event instances that the current user oversees,
    the date of each event instance, and the attendance
    """
    # db connection API
    #q = query()

    # build sql query
    sql_query = "\
        SELECT ev_ID, date, attendance \
        FROM event_instance \
        LEFT JOIN event ON event.ev_ID = event_instance.event \
        WHERE overseer = {0} \
        ORDER BY date DESC;".format(args[0])

    """
    # connect database
    with q.cursor(username = 'aq_admin', pwd = 'aq_Password01!') as cur:
        cur.execute(sql_query)

        res = cur.fetchall()
    """
    cursor.execute(sql_query)
    res = cursor.fetchall()
    return ['Event ID', 'Date', 'Attendance'], res

if __name__ == '__main__':
    view_my_events('123')
    check_facility_availability()
    check_aquarist_availability()
    assign_aquarist_to_event('e11', 'a1')
    assign_facility_to_event('e2', 'f1')
    log_event_attendance('e1000', 99)
    print(view_event_table('218363685'))
    print(view_event_instances('218363685'))


