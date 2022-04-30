from distutils.log import error
import mysql.connector
import time
from zmq import EVENT_LISTENING

database = mysql.connector.connect(
    host ="localhost",
    user="root",
    passwd="root",
    database = "aquarium"
)

cursor = database.cursor()

# view events report
def view_event(*arg): # type,start_date,end_date
    """
    Input parameters: type (enum),start_date(str),end_date(str) in order

    Function: Select event details and return result with colunm: ev_ID, 
    title, type, date, attendance. 

    """
    try:
        # sql query that reterive event detail 
        cursor.execute("select ev_ID, title, type, date, attendance \
                from event join event_instance on event.ev_ID = event_instance.event \
                where type ='{type}' and (date between '{start_date}' and '{end_date}')\
                order by attendance desc;".format(type=arg[0],start_date=arg[1],end_date=arg[2]))

        result=cursor.fetchall() #fetch sql result to array
        formatResult = "ev_ID        title        type             date                 attend" #declare column name

        for i in range(len(result)): #create a list for output
            formatResult=formatResult+"\n"+str(result[i])
        return formatResult

    except:
        errorNotice = "Error for pulling up event detail"
        return errorNotice

# create new event
def create_event(*arg):# ev_ID,title,type,overseer
    """
    Input parameters: ev_ID(char-6),title(str),type(enum),overseer(char-9) in order

    Function: Create new event by inserting to event table

    """
    try:
        cursor.execute("insert into event values ('{ev_ID}', '{title}', '{type}', null, '{overseer}');"\
            .format(ev_ID=arg[0],title=arg[1],type=arg[2],overseer=arg[3]))
        database.commit()
        return("Success to create event")
    except:
        return("Fail to create event,Check if event already exsits")

# view staff report
def view_staff_report():
    """
    Input parameters: N/A

    Function: Return report show curator-animal, event manager-event,
    aquraist-facility, aquraist-event

    """
    tempResult=[] # a temp array that store colunm name, report title and staff detail without formating 
    for i in range(4): # each round append one type of staff's detail
        if(i==0):
            column_title= "\n Curator Report \n curator   animal" # assign column name to str variable
            cursor.execute("select curator.name, animal.name\
	            from curator join animal on curator.st_ID=animal.curator;")
            tempResult.append(column_title) # insert column name
            tempResult.append(cursor.fetchall()) #follow by staff detail

        elif(i==1):
            column_title= "\n \nEvent Manager Report \nmanager      event"
            cursor.execute("select event_manager.name as mangaer_Name, event.title as event_title\
	            from event_manager join event on event_manager.st_ID = event.overseer;")
            tempResult.append(column_title)
            tempResult.append(cursor.fetchall())

        elif(i==2):
            column_title=("\n \nAquarist---Facility Report \naquarist   facility")
            cursor.execute("select aquarist.name as aquarist_Name, facility.name as facility_Name\
	            from aquarist, facility, maintain\
                where aquarist.st_ID=maintain.staff and maintain.facility = facility.fa_ID;")
            tempResult.append(column_title)
            tempResult.append(cursor.fetchall())

        else:
            column_title=("\n \nAcquarist---Event Report \naquarist      event")
            cursor.execute("select aquarist.name as aquarist_Name, event.title as event_Name\
	            from aquarist, event, work_on\
                where aquarist.st_ID = work_on.staff and work_on.event = event.ev_ID;")
            tempResult.append(column_title)
            tempResult.append(cursor.fetchall())

    complete_report="" # define an empty string for final formatted report
    for i in range(int(len(tempResult)/2)): # run 4 times in outerloop
        indexOfTitle=2*i #column name location are 0 2 4 6
        indexOfStaff = 2*i+1 # staff info location are 1 3 5 7
        complete_report = complete_report+tempResult[indexOfTitle] # insert related colunm name
        for j in range(len(tempResult[indexOfStaff])): # retierice and sort staff from list of the list
            complete_report=complete_report+"\n"+str(tempResult[indexOfStaff][j]) # format the staff line by line
    return complete_report

# Hire Staff
def hire_staff(*arg): # role,st_ID,name,phone,email
    """
    Input parameters: role{aquirst,curator,event_manger}, st_ID(char-9), name(str),
    phone(char-9), email(str)

    Function: Insert new staff to corresponding table

    """
    try:
        cursor.execute("insert into {role} values ('{st_ID}', NULL, '{name}', '{phone}', '{email}');"\
            .format(role=arg[0],st_ID=arg[1],name=arg[2],phone=arg[3],email=arg[4]))
        database.commit()
        return("Success to hire a new staff")
    except:
        return("Fail to hire new staff")

#Checking if Curator's animals have been reassigned before firing them
def animalAssignCheck(st_ID):
    """
    Input parameters: st_ID(char-9)

    Function: return boolean to check if animal has been reassign 
    to new staff before firing a curator

    """
    try:
        cursor.execute("select * from animal where animal.curator={st_ID};".format(st_ID=st_ID))
        test=cursor.fetchall()
        if(len(test)==0): # 0 indicate all animal has been reassigned
            return True 
        else:
            return False
    except:
        return("Error in animal assigning status checking")

#Checking if event manager's events have been reassigned before firing them
def eventAssignCheck(st_ID):
    """
    Input parameters: st_ID(char-9)

    Function: return boolean to check if event has been reassign 
    to new staff before firing a event manager
    """
    try:
        cursor.execute("select * from event where event.overseer = {st_ID};".format(st_ID=st_ID))
        test=cursor.fetchall()
        if(len(test)==0): # 0 indicate all events has been reassigned
            return True
        else:
            return False
    except:
        return("Error in event assigning status checking")

# Fire Staff
def fire_staff(st_ID):
    """
    Input parameters: st_ID(char-9)

    Function: fire staff after ensuring their task has been reassigned
    """
    staff=['curator','aquarist','event_manager']
    try:
        if(animalAssignCheck(st_ID)==True  and eventAssignCheck(st_ID)==True): # since aquarist is not in either tables, both remain true
            for i in staff: #locate the staff's role and fire
                cursor.execute("delete from {staff} where st_ID ='{st_ID}';".format(staff=i,st_ID=st_ID))
                database.commit()
            return("Success to fire staff")
        else:
            return("Fail to fire staff who still have duties assigned")
    except:
        return("Fail to fire staff due to exception")

# Refresh facility/animals
def refreshAll():
    """
    Input parameters: N/A

    Function: reset maintance status to false, reset feeding status to false,
    create new events to event_instance for a new date
    """
    try:
        # maintance status set to false
        cursor.execute("update facility_maint set facility_maint.maint_status= false;")

        # animal feed time set to 0
        cursor.execute("update animal set animal.status = 0;")

        # create event_instance for a new day
        localtime = time.localtime(time.time())
        newdate= str(localtime[0])+"-"+str(localtime[1])+"-"+str(localtime[2]) # retrieve current date

        cursor.execute("select event.ev_ID from event;") # retrieve all events from event table
        eventList = cursor.fetchall() # array of all event ID

        # insert each event to a new date in event_instance table
        for i in eventList:
            cursor.execute("insert into event_instance values ('{event_ID}', '{date}', null);".format(event_ID=i[0],date=newdate))
        database.commit()
        return("Success Update/Refresh")
    except:
        database.rolloback()
        return("Fail to refresh")

def selectTest(st_ID):
    """
    Input parameters: st_ID(char-9)

    Function: for testing to check which table the staff locate
    """
    staffList=['aquarist','curator','event_manager','general_manager']
    for i in range(4):
        cursor.execute("select st_ID, name from {staff} where st_ID='{st_ID}';".format(staff=staffList[i],st_ID=st_ID))
        foundStaff = cursor.fetchall() 
        if(len(foundStaff) !=0):
            print("In table {tableName} found ".format(tableName=staffList[i])+str(foundStaff))
            return []
####################################################################### TESTING AREA ########################################################

#print(view_staff_report())

#print(view_event("performance","2022-05-03","2022-05-04"))

#print(create_event('201008','crab show','performance','243910037'))

#print(hire_staff('curator','733289755','Johny','3224545','Johny@aquarium.com'))

#print(fire_staff('733289255'))

#print(refreshAll())

################################################################## Running Select Testing ####################################################

#allStaffID =['517465989','243910037','218363685','736289249','705628448','143705926','315400662','504236312','608059001','689620370','888748129','914191383','987153744']

#for i in allStaffID:
#    selectTest(i)

