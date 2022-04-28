import mysql.connector

database = mysql.connector.connect(
    host = 'localhost',
    user = 'aq_admin',
    password = 'aq_Password01!',
    database = 'aquarium'
)

cursor = database.cursor()

# Helper function to make sure the animal belongs to current user
def check_ownership(st_id, an_id):
    try:
        cursor.execute("SELECT curator FROM animal WHERE an_ID = '" + an_id + "';")
        return(st_id == str(cursor.fetchone()[0]))
    except:
        print("The animal ID you have entered does not exist")

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


########## Test
"""
user_id = '736289249'

an_id = '0000000000' # test a nonsense value
check_ownership(user_id, an_id)
remove_animal(user_id, an_id)
# Check animals
cursor.execute("SELECT * FROM animal;")
for i in cursor.fetchall():
    print(i)

an_id = '103001' # test an animal that does not belong to current user
check_ownership(user_id, an_id)
remove_animal(user_id, an_id)
# Check animals
cursor.execute("SELECT * FROM animal;")
for i in cursor.fetchall():
    print(i)

an_id = '101001' # test a valid animal
check_ownership(user_id, an_id)
remove_animal(user_id, an_id)
# Check animals
cursor.execute("SELECT * FROM animal;")
for i in cursor.fetchall():
    print(i)

an_id = '101001' # test a deleted animal
check_ownership(user_id, an_id)
remove_animal(user_id, an_id)
# Check animals
cursor.execute("SELECT * FROM animal;")
for i in cursor.fetchall():
    print(i)
"""