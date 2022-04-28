import mysql.connector
import time

from zmq import EVENT_LISTENING

db = mysql.connector.connect(
    host ="localhost",
    user="root",
    passwd="root",
    database = "aquarium"

)

mycursor = db.cursor()

# view events report
def view_event(*arg): # type,start_date,end_date
    mycursor.execute("select ev_ID, title, type, date, attendance \
        from event join event_instance on event.ev_ID = event_instance.event \
            where type ='{type}' and (date between '{start_date}' and '{end_date}')\
                order by attendance desc;".format(type=arg[0],start_date=arg[1],end_date=arg[2]))
    result=mycursor.fetchall()
    print(result)

# create new event
def create_event(*arg):# ev_ID,title,type,overseer
    try:
        mycursor.execute("insert into event values ('{ev_ID}', '{title}', '{type}', null, '{overseer}');"\
            .format(ev_ID=arg[0],title=arg[1],type=arg[2],overseer=arg[3]))
        db.commit()
        print("Success to create event")
    except:
        print("Fail to create event")

# view staff report
def view_staff_report():
    for i in range(4):
        if(i==0):
            print("\n Curator Report \n")
            mycursor.execute("select curator.name, animal.name\
	            from curator join animal on curator.st_ID=animal.curator;")
        elif(i==1):
            print("\n Event Manager Report \n")
            mycursor.execute("select event_manager.name as mangaer_Name, event.title as event_title\
	            from event_manager join event on event_manager.st_ID = event.overseer;")
        elif(i==2):
            print("\n Aquarist---Facility Report \n")
            mycursor.execute("select aquarist.name as aquarist_Name, facility.name as facility_Name\
	            from aquarist, facility, maintain\
                where aquarist.st_ID=maintain.staff and maintain.facility = facility.fa_ID;")
        else:
            print("\n Acquarist---Event Report \n")
            mycursor.execute("select aquarist.name as aquarist_Name, event.title as event_Name\
	            from aquarist, event, work_on\
                where aquarist.st_ID = work_on.staff and work_on.event = event.ev_ID;")
        result = mycursor.fetchall()
        print(result)

# Hire Staff
def hire_staff(*arg): # role,st_ID,name,phone,email
    try:
        mycursor.execute("insert into {role} values ('{st_ID}', NULL, '{name}', '{phone}', '{email}');"\
            .format(role=arg[0],st_ID=arg[1],name=arg[2],phone=arg[3],email=arg[4]))
        db.commit()
        print("Success to hire a new staff")
    except:
        print("Fail to hire new staff")

#Checking if Curator's animals have been reassigned before firing them
def animalAssignCheck(st_ID):
    mycursor.execute("select * from animal where animal.curator={st_ID};".format(st_ID=st_ID))
    test=mycursor.fetchall()
    if(len(test)==0):
        return True
    else:
        return False

#Checking if event manager's events have been reassigned before firing them
def eventAssignCheck(st_ID):
    mycursor.execute("select * from event where event.overseer = {st_ID};".format(st_ID=st_ID))
    test=mycursor.fetchall()
    if(len(test)==0):
        return True
    else:
        return False

# Fire Staff
def fire_staff(st_ID):
    staff=['curator','aquarist','event_manager']
    try:
        if(animalAssignCheck(st_ID)==True  and eventAssignCheck(st_ID)==True):
            for i in staff:
                mycursor.execute("delete from {staff} where st_ID ='{st_ID}';".format(staff=i,st_ID=st_ID))
                db.commit()
            print("Success to fire staff")
        else:
            print("Fail to fire staff who still have duties assigned")
    except:
        print("Fail to fire staff due to exception")

# Refresh facility/animals
def refreshAll():
    try:
        # maintance status set to false
        mycursor.execute("update facility_maint set facility_maint.maint_status= false;")
        db.commit()

        # animal feed time set to 0
        mycursor.execute("update animal set animal.status = 0;")
        db.commit()

        # create event_instance for a new day
        localtime = time.localtime(time.time())
        newdate= str(localtime[0])+"-"+str(localtime[1])+"-"+str(localtime[2]) # retrieve current date

        mycursor.execute("select event.ev_ID from event;") # retrieve all events from event table
        eventList = mycursor.fetchall() # array of all event ID

        # insert each event to a new date in event_instance table
        for i in eventList:
            mycursor.execute("insert into event_instance values ('{event_ID}', '{date}', null);".format(event_ID=i[0],date=newdate))
            db.commit()

        print("Success Update/Refresh")
    except:
        print("Fail to refresh")

####################################################################### TESTING AREA ########################################################

#mycursor.execute("select * from event where event.title='bad'")

#view_event("performance","2022-05-03","2022-05-04")

#mycursor.execute("select curator.name, animal.name from curator join animal on curator.st_ID=animal.curator;")

#view_staff_report()

#create_event('201003','crab show','performance','243910037')

#hire_staff('curator','733289255','Johny','3224545','Johny@aquarium.com')

#fire_staff('733289255')

# refreshAll()
