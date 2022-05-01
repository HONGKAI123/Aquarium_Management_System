from mysql import connector


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

        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.q.disconnect()
        return ['Facility','ID','Maintenance Time'],result
