import mysql.connector

database = mysql.connector.connect(
    host = 'localhost',
    user = 'aq_admin',
    password = 'aq_Password01!',
    database = 'aquarium'
)

cursor = database.cursor()

# check maintanence times
# arg = [user_id]
def check_maint_times(*arg):
    query = "\
    SELECT name AS 'Facility', fa_id AS 'ID', maint_time AS 'Maintenance Time' \
    FROM facility_maint \
    LEFT JOIN facility ON facility.fa_id = facility_maint.facility \
    LEFT JOIN maintain ON fa_id = maintain.facility \
    WHERE maint_status = FALSE \
    AND staff = '" + arg[0] + "' \
    ORDER BY maint_time ASC;"
    
    cursor.execute(query)

    #"""
    # Use block below if returning query results directly
    # RETURN FORMAT: list of tuples [('facility_name', 'fa_id', maint_time), ...]
    result = cursor.fetchall()
    #print(result)
    
    """
    # Use block below if returning list[rows[]]
    # RETURN FORMAT: list of lists [['facility_name', 'fa_id', maint_time], ...]
    result = []
    #result.append(['Facility', 'ID', 'Maintenance Time']) # Add header row if necessary
    for x in cursor.fetchall():
        result.append(list(x))
    # check results
    for i in result:
        print(i[0], ' ', i[1], ' ', i[2])
    """
    return result

# Update facility maintanence status
# arg = [user_id, fa_id, maint_time]
def maintain_facility(*arg):
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
        print("Facility " + arg[1] + " maintenance scheduled for " + arg[2] + " has been performed.")
    else:
        print("The selected facility + time slot combination does not exist.")

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