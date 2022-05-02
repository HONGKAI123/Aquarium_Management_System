# SJSU CMPE 138 Spring 2022 TEAM4

from all_query import query

def check_maint_times(*args):
    """
    arg = [user_id]

    
    query returns a list of maintenance times for facilities,
    filtered to only show which ones the current user is responsible for
    ordered by maintenance time slot, showing the earliest first


    """
    # db connection API
    q = query()

    # build SQL query
    sql_query = "\
    SELECT name AS 'Facility', fa_id AS 'ID', maint_time AS 'Maintenance Time' \
    FROM facility_maint \
    LEFT JOIN facility ON facility.fa_id = facility_maint.facility \
    LEFT JOIN maintain ON fa_id = maintain.facility \
    WHERE maint_status = FALSE \
    AND staff = '{0}' \
    ORDER BY maint_time ASC;".format(args[0])

    # connect to API
    with q.cursor(username = 'root', pwd = 'lucifer') as cur:
        cur.execute(sql_query)
        
        res = cur.fetchall()

    # add column names to result and return
    return ['Facility Name', 'ID', 'Maintenance Time'], res



def maintain_facility(*args):
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

    # connect to API
    with q.cursor(username = 'root', pwd = 'lucifer') as cur:
        cur.execute(sql_query)

        q.conn.commit()

        res = cur.rowcount

    # whether the data is modified
    return True if res > 0 else False