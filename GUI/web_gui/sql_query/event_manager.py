# *arg
import mysql.connector

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
    sql_query = "SELECT * FROM Event WHERE overseer = " + "'" + args[0] + "'"
    cursor.execute(sql_query)
    result = cursor.fetchall()
    print(result)


def check_aquarist_availability():     #COUNT(*) event_count?
    """
    list all workers and numbers of events that the person is working on
    """
    # list all people, count events..
    sql_query = "SELECT staff, COUNT(*) event_count " \
                "FROM Work_on " \
                "GROUP BY staff " \
                "ORDER BY COUNT(*) DESC"
    cursor.execute(sql_query)
    result = cursor.fetchall()
    print(result)


def assign_aquarist_to_event(*args):
    """
    assign aquarist(id) to event(id) 
    """
    
    aquarist_ID = args[0]
    event_ID = args[1]
    sql_query = "INSERT INTO Work_on VALUES (" + "'" + event_ID + "','" + aquarist_ID + "')"  #aquarist_ID?
    try:
        cursor.execute(sql_query)
        database.commit()
        print('aquarist assigned successfully')
    except:
        print('failed to assign aquarist')
    print(sql_query)


def check_facility_availability():
    """
    list all facilities that is not hosting an event
    """
    sql_query = "SELECT * from Facility WHERE fa_ID NOT IN (SELECT facility from Event )"  # In where facility.... = event......
    cursor.execute(sql_query)
    result = cursor.fetchall()
    print(result)


def assign_facility_to_event(*args):
    """
    assign facility(id) to event(id) 
    """
    event_ID = args[0]
    facility_ID = args[1]
    sql_query = "UPDATE Event SET facility = " + "'" + facility_ID + "' " + \
                "WHERE ev_ID =" + "'" + event_ID + "'"
    try:
        cursor.execute(sql_query)
        database.commit()
        print('facility assigned successfully')
    except:
        print('failed to assign facility')
    print(sql_query)


def log_event_attendance(*args):
    """
    Input: recorded_attendance, event_ID
    Update an event's attendance number to an Event_instance.
    """
    event_ID = args[0]
    recorded_attendance = args[1]
    sql_query = "UPDATE Event_instance SET attendance = " + str(recorded_attendance) + \
                " WHERE event = " + "'" + event_ID + "'"
    try:
        cursor.execute(sql_query)
        database.commit()
        print('event log updated successfully')
    except:
        print('failed to update event log')
    print(sql_query)


if __name__ == '__main__':
    view_my_events('123')
    check_facility_availability()
    check_aquarist_availability()
    assign_aquarist_to_event('e11', 'a1')
    assign_facility_to_event('e2', 'f1')
    log_event_attendance('e1000', 99)