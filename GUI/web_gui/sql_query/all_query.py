# SJSU CMPE 138 Spring 2022 TEAM6
from mysql import connector
import time


class dbHelper():
    def timedeltaTOstr(self):
        pass


class query():
    def cursor(self, username: str = 'root', pwd: str = "lucifer"):
        self.conn = connector.connect(
            host = 'localhost',
            user = username,
            password = pwd,
            database = 'aquarium')
        return self.conn.cursor()

    def disconnect(self):
        self.cursor().close()
        self.conn.disconnect()

class aquarist():
    def __init__(self):
        self.q = query()
        self.cursor = self.q.cursor()

    # check maintanence times
    # arg = [user_id]
    def check_maint_times(self, *arg):
        """
        input: string: user_id
        :return list of column name, queryset
        """

        query = "SELECT name AS 'Facility', fa_id AS 'ID', maint_time AS 'Maintenance Time' FROM facility_maint \
        LEFT JOIN facility ON facility.fa_id = facility_maint.facility \
        LEFT JOIN maintain ON fa_id = maintain.facility \
        WHERE maint_status = FALSE \
        AND staff = '" + arg[0] + "' \
        ORDER BY maint_time ASC;"
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.q.disconnect()

        except connector.Error as e:
            result = e
        finally:
            return ['Facility', 'ID', 'Maintenance Time'], result

    def maintain_facility(self,*args):
        """
        arg = [fa_id, maint_time]
        returns success or error message

        take input of facility id and maintanence time slot,
        change the maintanence status to TRUE for that instance
        """
        # db connection API
        q = query()

        # build SQL query
        sql_query = "\
            UPDATE facility_maint \
            SET maint_status = true \
            WHERE facility = '{0}' \
            AND maint_time = '{1}';".format(args[0], args[1])
        print('sql',sql_query)
        # connect to API
        with q.cursor() as cur:
            cur.execute(sql_query)
            q.conn.commit()
            res = cur.rowcount

        # whether the data is modified
        return True if res > 0 else False


class director():
    # view events report
    def view_event(self, *arg):  # type,start_date,end_date
        """
        View events by selecting
        :param args: type (enum),start_date(str),end_date(str)

        :return: array of selected event detail
        """
        # call db connection API
        q = query()

        # sql query that reterive event detail
        sql_query = "select ev_ID, title, type, date, attendance \
                    from event join event_instance on event.ev_ID = event_instance.event \
                    where type ='{type}' and (date between '{start_date}' and '{end_date}')\
                    order by attendance desc;".format(type = arg[0], start_date = arg[1], end_date = arg[2])

        with q.cursor() as cur:
            cur.execute(sql_query)
            # catch return result
            res = cur.fetchall()

        return ['Event ID', 'title', 'type', 'date', 'attend'], res

    # create new event
    def create_event(self, *arg):  # ev_ID,title,type,overseer
        """
        Create new event by inserting
        :param args: ev_ID(char-6), title(str),type(enum),overseer(char-9)

        :return: has created event into database
        """
        # call db connection API
        q = query()

        # sql query that create new event to db
        sql_query = "insert into event values ('{ev_ID}', '{title}', '{type}', null, '{overseer}');" \
            .format(ev_ID = arg[0], title = arg[1], type = arg[2], overseer = arg[3])
        print(sql_query, "sql")
        with q.cursor() as cur:
            cur.execute(sql_query)

            # submit change to database
            q.conn.commit()

            # catch return result
            res = cur.rowcount

        return True if res > 0 else False

    # for Delete Event Button
    def cancel_event(self, ev_ID):
        """
        :param args: ev_ID(char-6)

        :return: has removed event from database
        """

        # call db connection API
        q = query()
        sql_query = "delete from event where ev_ID = '{ev_ID}';".format(ev_ID = ev_ID)

        with q.cursor() as cur:
            cur.execute(sql_query)
            q.conn.commit()
            res = cur.rowcount

        return True if res > 0 else False

    # view staff report
    def view_staff_report(self):
        """
        :param args: N/A

        :return: array of selected report on curator-animal,
        event manager-event, aquraist-facility, aquraist-event
        """

        q = query()

        with q.cursor() as cur:
            column = []
            finalResult = []  # an array that store colunm name, report title and staff detail without formating
            for i in range(4):  # each round append one type of staff's detail
                if (i == 0):
                    sql_query = "select curator.st_ID,curator.name, animal.name\
                        from curator join animal on curator.st_ID=animal.curator;"
                    cur.execute(sql_query)
                    res = cur.fetchall()
                    column_title = ['ID', 'Curator', 'Animal']  # assign column name to str variable
                    finalResult.append(
                        column_title)  # insert column name                    finalResult.extend(res)  # follow by staff detail
                    finalResult.append(res)

                elif (i == 1):
                    sql_query = "select event_manager.st_ID,event_manager.name as mangaer_Name, event.title as event_title\
                    from event_manager join event on event_manager.st_ID = event.overseer;"
                    cur.execute(sql_query)
                    column_title = ['ID', 'Manager', 'Event']
                    res = cur.fetchall()
                    finalResult.append(column_title)
                    finalResult.append(res)

                elif (i == 2):
                    sql_query = "select aquarist.st_ID,aquarist.name as aquarist_Name, facility.name as facility_Name\
                    from aquarist, facility, maintain\
                    where aquarist.st_ID=maintain.staff and maintain.facility = facility.fa_ID;"
                    cur.execute(sql_query)
                    column_title = ['ID', 'Aquarist', 'Facility']
                    res = cur.fetchall()
                    finalResult.append(column_title)
                    finalResult.append(res)

                else:
                    sql_query = "select aquarist.st_ID,aquarist.name as aquarist_Name, event.title as event_Name\
                    from aquarist, event, work_on\
                    where aquarist.st_ID = work_on.staff and work_on.event = event.ev_ID;"
                    cur.execute(sql_query)
                    column_title = ['ID', 'Aquarist', 'Event']
                    res = cur.fetchall()
                    finalResult.append(column_title)
                    finalResult.append(res)

        return finalResult

    # Hire Staff
    def hire_staff(self, *arg):  # role,st_ID,name,phone,email
        """
        :param args: role{aquirst,curator,event_manger}, st_ID(char-9),
        name(str), phone(char-9), email(str),password(str)

        :return: has added staff to database

        """
        # call db connection API
        q = query()

        # sql query that create new staff to db
        sql_query = "insert into {role} values ('{st_ID}', md5('{pwd}'), '{name}', '{phone}', '{email}');" \
            .format(role = arg[0], st_ID = arg[1], name = arg[2], phone = arg[3], email = arg[4], pwd = arg[5])
        with q.cursor() as cur:
            cur.execute(sql_query)
            # submit change to database
            q.conn.commit()

            # catch return result
            res = cur.rowcount

        return True if res > 0 else False

    # Checking if Curator's animals have been reassigned before firing them
    def animalAssignCheck(self, st_ID):
        """
        :param args: st_ID(char-9)

        :return: has an valid reassignment
        """
        # call db connection API
        q = query()

        # sql query that reterive animal and curator from db
        sql_query = "select * from animal where animal.curator={st_ID};".format(st_ID = st_ID)

        with q.cursor() as cur:
            cur.execute(sql_query)
            # catch return result
            res = cur.fetchall()

        return True if len(res) == 0 else False  # length=0 indicates reassigned all tasks

    # Checking if event manager's events have been reassigned before firing them
    def eventAssignCheck(self, st_ID):
        """
        :param args: st_ID(char-9)

        :return: has an valid reassignment
        """

        # call db connection API
        q = query()

        # sql query that reterive event and manager from db
        sql_query = "select * from event where event.overseer = {st_ID};".format(st_ID = st_ID)

        with q.cursor() as cur:
            cur.execute(sql_query)
            # catch return result
            res = cur.fetchall()

        return True if len(res) == 0 else False  # length=0 indicates reassigned all tasks

    # Fire Staff
    def fire_staff(self, st_ID):
        """
        :param args: st_ID(char-9)

        :return: has removed staff from database
        """

        staff = ['curator', 'aquarist', 'event_manager']

        # call db connection API
        q = query()

        with q.cursor() as cur:
            # since aquarist is not in either tables, both remain true
            if (self.animalAssignCheck(st_ID) == True and self.eventAssignCheck(st_ID) == True):
                for i in staff:  # locate the staff's role and fire
                    # sql query that delete staff from db
                    sql_query = "delete from {staff} where st_ID ='{st_ID}';".format(staff = i, st_ID = st_ID)
                    cur.execute(sql_query)

                    # submit change to database
                    q.conn.commit()

                return True
            else:
                return False

    # Refresh events/facility/animals
    def refreshAll(self):
        """
        :param args: N/A

        :return: has update requirement
        """
        q = query()

        with q.cursor() as cur:
            sql_query_maintance = "update facility_maint set facility_maint.maint_status= false;"
            cur.execute(sql_query_maintance)

            sql_query_feeding = "update animal set animal.status = 0;"
            cur.execute(sql_query_feeding)

            # create event_instance for a new day
            localtime = time.localtime(time.time())
            newdate = str(localtime[0]) + "-" + str(localtime[1]) + "-" + str(localtime[2])  # retrieve current

            sql_query_getEvent = "select event.ev_ID from event;"
            cur.execute(sql_query_getEvent)
            eventList = cur.fetchall()

            for i in eventList:
                sql_query_renewEvent = "insert into event_instance values ('{event_ID}', '{date}', null);".format(
                    event_ID = i[0], date = newdate)
                cur.execute(sql_query_renewEvent)
            # submit change to database
            q.conn.commit()

            # catch return result
            res = cur.rowcount

        return True if res > 0 else False




class curator():
    # Helper function to make sure the animal belongs to current user
    # return T/F
    def check_ownership(self, st_id, an_id):
        ls = ['Curator']
        try:
            q = query()
            with q.cursor() as cur:
                cur.execute("SELECT curator FROM animal WHERE an_ID = '" + an_id + "';")
                return (st_id == str(cur.fetchone()[0]))
        except:
            print("The animal ID you have entered does not exist")
            # return ls,result

    # Check animal status
    def check_an_Status(self):
        ls = ["Animal Name", "Animal ID", "Status"]
        sql_query = "\
        SELECT name,an_id,Status \
        FROM animal;"

        q = query()
        with q.cursor() as cur:
            cur.execute(sql_query)
            res = cur.fetchall()
        # for result in res:
        #     print(result)
        return ls, res

    # Update animal status (set to 1)
    # arg = [an_ID]
    def update_an_Status(self, *arg):
        sql_query = " \
        UPDATE animal \
        SET status = true \
        WHERE an_ID = '" + arg[0] + "';"

        q = query()
        with q.cursor() as cur:
            cur.execute(sql_query)
            # 提交修改后的语句到数据库
            q.conn.commit()

            # 获取被修改的行数
            res = cur.rowcount

        return True if res > 0 else False

    # Chekc facility availability for adding new animals
    # arg = [species]
    def check_spare_facility(self, *arg):
        ls = ['Facility ID', 'Facility Name']
        print("sql_check_spare_facility", arg[0])
        sql_query = "SELECT fa_ID, f.name \
        FROM facility f \
        left join animal on f.fa_id = animal.habitat \
        where species = '" + arg[0] + "' or (f.fa_ID not in (select habitat from animal group by habitat) and f.fa_ID not in (select e.facility from event e group by e.facility)) \
        group by fa_ID;"

        q = query()
        with q.cursor() as cur:
            cur.execute(sql_query)
            results = cur.fetchall()
        # for result in results:
        #     print(result)

        return ls, results

    # Add new animals
    # arg = [an_ID, name, species,st_id, habitat]
    def add_new_animal(self, *arg):
        # try:
        sql_query = "INSERT INTO animal VALUES ('{}','{}','{}',0,'{}','{}');".format(arg[0], arg[1], arg[2],
                                                                                     arg[3, arg[4]])
        q = query()
        with q.cursor() as cur:
            cur.execute(sql_query)
            q.conn.commit()

            res = cur.rowcount

        return True if res > 0 else False

    # Remove existing animal by an_ID
    # arg = [st_ID, an_ID]
    def remove_animal(self, *arg):

        # Make sure the animal being removed belongs to current curator
        if self.check_ownership(arg[0], arg[1]) == True:
            sql_query = "\
            DELETE FROM animal \
            WHERE an_ID = '" + arg[1] + "';"

        q = query()
        with q.cursor() as cur:
            cur.execute(sql_query)
            # 获得返回结果
            res = cur.rowcount

        return True if res > 0 else False
