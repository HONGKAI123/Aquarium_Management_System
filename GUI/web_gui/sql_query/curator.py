import mysql.connector

database = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'batcat2022',
    database = 'aquarium'
    # Change the password above to your own localhost password
)

cursor = database.cursor()

# Helper function to make sure the animal belongs to current user
def check_ownership(st_id, an_id):
    try:
        cursor.execute("SELECT curator FROM animal WHERE an_ID = '" + an_id + "';")
        return(st_id == str(cursor.fetchone()[0]))
    except:
        print("The animal ID you have entered does not exist")

# Check animal status
def check_an_Status():
    query = "\
    SELECT * \
    FROM animal;"

    cursor.execute(query)

    results = cursor.fetchall()
    for result in results:
        print(result)


#Update animal status (set to 1)
# arg = [an_ID]
def update_an_Status(*arg):
    query = " \
    UPDATE animal \
    SET status = true \
    WHERE an_ID = '" + arg[0] + "';"

    cursor.execute(query)
    database.commit()
    print("Animal with an_ID " + arg[0] + " has been fed.")


#Chekc facility availability for adding new animals
# arg = [species]
def check_spare_facility(*arg):
    query = "\
    SELECT fa_ID, f.name \
    FROM facility f \
    left join animal on f.fa_id = animal.habitat \
    where species = '" + arg[0] + "' or (f.fa_ID not in (select habitat from animal group by habitat) and f.fa_ID not in (select e.facility from event e group by e.facility)) \
    group by fa_ID;"

    cursor.execute(query)
    results = cursor.fetchall()
    for result in results:
        print(result)


#Add new animals
# arg = [an_ID, name, species, habitat]
def add_new_animal(*arg):
    #try:
    query = "\
    INSERT INTO animal VALUES ('" + arg[0] + "','" + arg[1] + "','" + arg[2] + "', 0, '705628448','" + arg[3] + "'); "

    cursor.execute(query)
    database.commit()
    print("Animal with an_ID " + arg[0] + " has been added.")
    #except:
    #    print("Fail to add animal")


# Remove existing animal by an_ID
# arg = [st_ID, an_ID]
def remove_animal(*arg):
    # Make sure the animal being removed belongs to current curator
    if check_ownership(arg[0], arg[1]) == True:
        query = "\
        DELETE FROM animal \
        WHERE an_ID = '" + arg[1] + "';"

        cursor.execute(query)
        database.commit()
        print("Animal " + str(arg[1]) + " is no longer with us.")
    else:
        print("Please check staff ID and animal ID to make sure they are both valid and related")


# Testing
#arg:
an_ID = '103001'
species = 'spotted seal'
st_ID = '705628448'

# Check animal status
check_an_Status()

#Update animal status (set to 1)
update_an_Status(an_ID)
check_an_Status()

#Chekc facility availability for adding new animals
check_spare_facility(species)


an_ID1 = '106001'
name = 'Winston'
species1 = 'bottlenose dolphin'
habitat = '100005'
st_ID1 = '705628448'

#Add new animals
add_new_animal(an_ID1, name, species1, habitat)
check_an_Status()

#remove animal
remove_animal(st_ID1, an_ID1)
check_an_Status()