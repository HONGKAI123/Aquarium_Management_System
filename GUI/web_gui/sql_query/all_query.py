from mysql import connector


class dbHelper():
    def timedeltaTOstr(self):
        pass

class query():
    def cursor(self):
        self.conn = connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'lucifer',
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
        self.row = 0
        input_match = False
        for i in self.check_maint_times(arg[0])[1]:
            if str(i[1]) == str(arg[1]) and str(i[2]) == str(arg[2]):
                input_match = True

        try:
            if input_match == True:
                query = "UPDATE facility_maint \
                SET maint_status = true \
                WHERE facility = '" + arg[1] + "' \
                AND maint_time = '" + arg[2] + "';"
            print('sql ok')
            self.cursor.execute(query)
            self.row = self.cursor.rowcount()
            print("????")
            self.q.conn.commit()
            self.q.disconnect()
        except connector.Error as e:
            print (e)

        finally:
            return True if self.row > 0 else False

