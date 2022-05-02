# SJSU CMPE 138 Spring 2022 TEAM4
import time
from all_query import query

# view events report
def view_event(*arg): # type,start_date,end_date
    """
    View events by selecting
    :param args: type (enum),start_date(str),end_date(str)

    :return: array of selected event detail
    """
    # call db connection API
    q=query()

     # sql query that reterive event detail
    sql_query = "select ev_ID, title, type, date, attendance \
                from event join event_instance on event.ev_ID = event_instance.event \
                where type ='{type}' and (date between '{start_date}' and '{end_date}')\
                order by attendance desc;".format(type=arg[0],start_date=arg[1],end_date=arg[2])

    with q.cursor() as cur:
        cur.execute(sql_query)
        # catch return result
        res = cur.fetchall()

    return ['ev_ID','title','type','date','attend'], res


# create new event
def create_event(*arg):# ev_ID,title,type,overseer
    """
    Create new event by inserting
    :param args: ev_ID(char-6), title(str),type(enum),overseer(char-9)

    :return: has created event into database
    """
    # call db connection API
    q=query()

     # sql query that create new event to db
    sql_query = "insert into event values ('{ev_ID}', '{title}', '{type}', null, '{overseer}');"\
            .format(ev_ID=arg[0],title=arg[1],type=arg[2],overseer=arg[3])

    with q.cursor() as cur:
        cur.execute(sql_query)

        #submit change to database
        q.conn.commit()

        # catch return result
        res = cur.rowcount

    return True if res > 0 else False

# view staff report
def view_staff_report():
    """
    :param args: N/A

    :return: array of selected report on curator-animal,
    event manager-event, aquraist-facility, aquraist-event
    """

    q = query()

    with q.cursor() as cur:

        finalResult=[] # an array that store colunm name, report title and staff detail without formating
        for i in range(4): # each round append one type of staff's detail
            if(i==0):
                sql_query = "select curator.name, animal.name\
	                from curator join animal on curator.st_ID=animal.curator;"
                cur.execute(sql_query)
                res = cur.fetchall()
                column_title= ['Curator','Animal'] # assign column name to str variable
                finalResult.append(column_title) # insert column name
                finalResult.append(res) #follow by staff detail

            elif(i==1):
                sql_query = "select event_manager.name as mangaer_Name, event.title as event_title\
	            from event_manager join event on event_manager.st_ID = event.overseer;"
                cur.execute(sql_query)
                column_title=['Manager','Event']
                res = cur.fetchall()
                finalResult.append(column_title)
                finalResult.append(res)

            elif(i==2):
                sql_query = "select aquarist.name as aquarist_Name, facility.name as facility_Name\
	            from aquarist, facility, maintain\
                where aquarist.st_ID=maintain.staff and maintain.facility = facility.fa_ID;"
                cur.execute(sql_query)
                column_title=['Aquarist','Facility']
                res = cur.fetchall()
                finalResult.append(column_title)
                finalResult.append(res)

            else:
                sql_query="select aquarist.name as aquarist_Name, event.title as event_Name\
	            from aquarist, event, work_on\
                where aquarist.st_ID = work_on.staff and work_on.event = event.ev_ID;"
                cur.execute(sql_query)
                column_title=['Aquarist','Event']
                res = cur.fetchall()
                finalResult.append(column_title)
                finalResult.append(res)

    return finalResult

# Hire Staff
def hire_staff(*arg): # role,st_ID,name,phone,email
    """
    :param args: role{aquirst,curator,event_manger}, st_ID(char-9),
    name(str), phone(char-9), email(str)

    :return: has added staff to database

    """
    # call db connection API
    q=query()

     # sql query that create new staff to db
    sql_query = "insert into {role} values ('{st_ID}', NULL, '{name}', '{phone}', '{email}');"\
            .format(role=arg[0],st_ID=arg[1],name=arg[2],phone=arg[3],email=arg[4])

    with q.cursor() as cur:
        cur.execute(sql_query)

        #submit change to database
        q.conn.commit()

        # catch return result
        res = cur.rowcount

    return True if res > 0 else False


#Checking if Curator's animals have been reassigned before firing them
def animalAssignCheck(st_ID):
    """
    :param args: st_ID(char-9)

    :return: has an valid reassignment
    """
    # call db connection API
    q=query()

     # sql query that reterive animal and curator from db
    sql_query = "select * from animal where animal.curator={st_ID};".format(st_ID=st_ID)

    with q.cursor() as cur:
        cur.execute(sql_query)
        # catch return result
        res = cur.fetchall()

    return True if len(res)==0 else False #length=0 indicates reassigned all tasks

#Checking if event manager's events have been reassigned before firing them
def eventAssignCheck(st_ID):
    """
    :param args: st_ID(char-9)

    :return: has an valid reassignment
    """

    # call db connection API
    q=query()

     # sql query that reterive event and manager from db
    sql_query = "select * from event where event.overseer = {st_ID};".format(st_ID=st_ID)

    with q.cursor() as cur:
        cur.execute(sql_query)
        # catch return result
        res = cur.fetchall()

    return True if len(res)==0 else False #length=0 indicates reassigned all tasks

# Fire Staff
def fire_staff(st_ID):
    """
    :param args: st_ID(char-9)

    :return: has removed staff from database
    """

    staff=['curator','aquarist','event_manager']

    # call db connection API
    q=query()

    with q.cursor() as cur:
        # since aquarist is not in either tables, both remain true
        if(animalAssignCheck(st_ID)==True and eventAssignCheck(st_ID)==True):
            for i in staff: #locate the staff's role and fire
                # sql query that delete staff from db
                sql_query = "delete from {staff} where st_ID ='{st_ID}';".format(staff=i,st_ID=st_ID)
                cur.execute(sql_query)

                #submit change to database
                q.conn.commit()

            return True
        else:
            return False

# Refresh events/facility/animals
def refreshAll():
    """
    :param args: N/A

    :return: has update requirement
    """
    q=query()

    with q.cursor() as cur:

        sql_query_maintance = "update facility_maint set facility_maint.maint_status= false;"
        cur.execute(sql_query_maintance)

        sql_query_feeding = "update animal set animal.status = 0;"
        cur.execute(sql_query_feeding)

         # create event_instance for a new day
        localtime = time.localtime(time.time())
        newdate= str(localtime[0])+"-"+str(localtime[1])+"-"+str(localtime[2]) # retrieve current

        sql_query_getEvent = "select event.ev_ID from event;"
        cur.execute(sql_query_getEvent)
        eventList = cur.fetchall()

        for i in eventList:
            sql_query_renewEvent = "insert into event_instance values ('{event_ID}', '{date}', null);".format(event_ID=i[0],date=newdate)
            cur.execute(sql_query_renewEvent)
        #submit change to database
        q.conn.commit()

        # catch return result
        res = cur.rowcount

    return True if res > 0 else False

# Testing function to locate staff(This is only for director.py's internal testing)
def selectTest(st_ID):
    """
    :param args: st_ID(Char-9)

    :return: print staff and his table in db
    """
    staffList=['aquarist','curator','event_manager','general_manager']
    q=query()
    with q.cursor() as cur:
        for i in range(4):
            cur.execute("select st_ID, name from {staff} where st_ID='{st_ID}';".format(staff=staffList[i],st_ID=st_ID))
            foundStaff = cur.fetchall()
            if(len(foundStaff) !=0):
                print("In table {tableName} found ".format(tableName=staffList[i])+str(foundStaff))
####################################################################### TESTING AREA ########################################################

if __name__ == '__main__':
    print(view_staff_report())

#print(view_event("performance","2022-05-03","2022-05-04"))

#print(create_event('301015','snake show','performance','243910037'))

#print(hire_staff('curator','132049705','judy','3224545','Johny@aquarium.com'))

#print(fire_staff('132049705'))

#print(refreshAll())

################################################################## Running Select Testing ####################################################

#allStaffID =['517465989','243910037','218363685','736289249','705628448','143705926','315400662','504236312','608059001','689620370','888748129','914191383','987153744']

#for i in allStaffID:
#    selectTest(i)


