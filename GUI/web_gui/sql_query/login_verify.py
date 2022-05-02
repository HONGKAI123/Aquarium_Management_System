import mysql.connector
import hashlib


from all_query import query

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

    table_list = ['aquarist','curator','event_manager','general_manager']
    sql_query = "SELECT hashed_pw FROM {} WHERE st_id = '{}';"

    # sql_query_list = []
    # for idx,i in enumerate(table_list):
    #     print(idx,i)
    #     sql_query_list.append(sql_query.format(i))
    #     # sql_query_list.append(sql_query.format(i[idx]))
    #
    # print(sql_query_list)



    name = 'Bender'
    q = query()

    with q.cursor(username = 'root', pwd = 'lucifer') as cur:
        for i in table_list:
            cur.execute(sql_query.format(i,name))
            res = cur.fetchall()
            print(res)

    # try:
    #     stored_pw = (cursor.fetchone()[0])
    # except:
    #     print('User does not exist in selected role')
    #     return None
    #
    # #stored_pw = get_pw_hash(arg[0], arg[1])
    #
    # if(stored_pw == hash_input(arg[2])):
    #     return((arg[0], arg[1]))
    # else:
    #     print('Invalid staff ID + password combination')
    #     return None

if __name__ == '__main__':
    verify_user('a')