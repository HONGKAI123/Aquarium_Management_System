import mysql.connector

database = mysql.connector.connect(
    host = 'localhost',
    user = 'aq_admin',
    password = 'aq_Password01!',
    database = 'aquarium'
)

cursor = database.cursor()


def check_maint_times(*arg):
    """
    arg = [user_id]
    returns list of list
        each inner list represents a row, the first row being the column names
        columns returned: Facility Name, Facility ID, Maintenance Time
    
    query returns a list of maintenance times for facilities,
    filtered to only show which ones the current user is responsible for
    ordered by maintenance time slot, showing the earliest first

    for example: user is 608059001
    returns: 
        [['Facility', 'ID', 'Maintenance Time'], 
        ['whale tank', '100001', datetime.timedelta(seconds=28800)], 
        ['shark tank', '100002', datetime.timedelta(seconds=32400)], 
        ['seal beach', '100003', datetime.timedelta(seconds=36000)], 
        ['whale tank', '100001', datetime.timedelta(seconds=72000)], 
        ['seal beach', '100003', datetime.timedelta(seconds=79200)]]
    """

    query = "\
    SELECT name AS 'Facility', fa_id AS 'ID', maint_time AS 'Maintenance Time' \
    FROM facility_maint \
    LEFT JOIN facility ON facility.fa_id = facility_maint.facility \
    LEFT JOIN maintain ON fa_id = maintain.facility \
    WHERE maint_status = FALSE \
    AND staff = '" + arg[0] + "' \
    ORDER BY maint_time ASC;"
    
    cursor.execute(query)

    """
    # Use block below if returning query results directly
    # RETURN FORMAT: list of tuples [('facility_name', 'fa_id', maint_time), ...]
    result = cursor.fetchall()
    #print(result)
    
    """
    # Use block below if returning list[rows[]]
    # RETURN FORMAT: list of lists [['facility_name', 'fa_id', maint_time], ...]
    result = []
    result.append(['Facility', 'ID', 'Maintenance Time']) # Add header row
    for x in cursor.fetchall():
        result.append(list(x))
    # check results
    """
    for i in result:
        print(i[0], ' ', i[1], ' ', i[2])
    """
    return result



def maintain_facility(*arg):
    """
    arg = [user_id, fa_id, maint_time]
    returns success or error message

    take input of facility id and maintanence time slot,
    check to make sure the input is valid for the current user,
    then change the maintanence status to TRUE for that instance

    for example, aquarist 608059001 chooses facility 100001 at 8:00:00,
    this function will update the maint_status for that facility at
    that time slot to TRUE, and returns a success message
    if aquarist 608059001 chooses a facility 100002 at 8:00:00,
    which does not exist, then a message will be returned to
    indicate that combination does not exist
    """
    # Check if the fa_id and maint_time combo exists for current user
    input_match = False
    for i in check_maint_times(arg[0]):
        if str(i[1]) == str(arg[1]) and str(i[2]) == str(arg[2]):
            input_match = True

    if input_match == True:
        query = "\
        UPDATE facility_maint \
        SET maint_status = true \
        WHERE facility = '" + arg[1] + "' \
        AND maint_time = '" + arg[2] + "';"

        cursor.execute(query)
        database.commit()
        return("Facility " + arg[1] + " maintenance scheduled for " + arg[2] + " has been performed.")
    else:
        return("The selected facility + time slot combination does not exist.")

""""
### Testing ###
user_id = '987153744'
fac_id = '300001'
time_slot = '12:00:00'

print(check_maint_times(user_id))

# Check maint table
# arg = [fa_id]
def check_maintain_result(*arg):
    query = "\
    SELECT * \
    FROM facility_maint \
    WHERE facility = " + arg[0] + ";"
    
    cursor.execute(query)
    
    print(cursor.fetchall())

check_maintain_result(fac_id)

maintain_facility(user_id, fac_id, time_slot)
check_maintain_result(fac_id)

# Reset maint
def reset_maint_status():
    query = "\
    UPDATE facility_maint \
    SET maint_status = false"
    
    cursor.execute(query)
    database.commit()

reset_maint_status()
check_maintain_result(fac_id)
"""