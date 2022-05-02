import mysql.connector
import hashlib

database = mysql.connector.connect(
    host = 'localhost',
    user = 'aq_admin',
    password = 'aq_Password01!',
    database = 'aquarium'
)

cursor = database.cursor()

def hash_input(input_str):
    """
    HELPER FUNCTION
    take a manually entered string value
    RETURN its hash value (MD5)
    """
    return(hashlib.md5(input_str.encode())).hexdigest().encode()

def verify_user(*arg):
    """
    arg = [role table, user name, password]
    RETURN a tuple of (role_table_name, st_id) if login info is valid
    RETURN None if user is not in the designated role table or password is wrong
    """
    
    query = "SELECT hashed_pw FROM " + str(arg[0]) + " WHERE st_id = " + str(arg[1]) + ";"
    
    cursor.execute(query)
    
    try:
        stored_pw = (cursor.fetchone()[0])
    except:
        print('User does not exist in selected role')
        return None
    
    #stored_pw = get_pw_hash(arg[0], arg[1])
    
    if(stored_pw == hash_input(arg[2])):
        return((arg[0], arg[1]))
    else:
        print('Invalid staff ID + password combination')
        return None