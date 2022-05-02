from mysql import connector


class dbHelper():
    def timedeltaTOstr(self):
        pass

class query():
    def cursor(self,username:str = 'root',pwd:str= "lucifer"):
        self.conn = connector.connect(
            host = 'localhost',
            user = username,
            password =pwd,
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

    def maintain_facility(self, *arg):
        # todo effected row not return
        """
        Update facility maintanence status
        :param arg:
        [user_id, fa_id, maint_time]
        user_id string :'987153744'
        fac_id string : '300001'
        time_slot type??? : '12:00:00'
        :return:
        """
        # Check if the fa_id and maint_time combo exists for current user
        input_match = False
        for i in self.check_maint_times(arg[0])[1]:
            if str(i[1]) == str(arg[1]) and str(i[2]) == str(arg[2]):
                input_match = True

        try:
            if input_match == True:
                query = "UPDATE facility_maint \
                SET maint_status = 1 \
                WHERE facility = '{0}' \
                AND maint_time = '{1}';".format(arg[1],arg[2])
            cursor = self.cursor()
            cursor.execute(query)

            # print(self.cursor.rowcount)
            print(query)
            print('?')
            self.q.conn.commit()
            self.q.disconnect()
        except connector.Error as e:
            print (e)

        finally:
            return True if self.cursor.rowcount > 0 else False

