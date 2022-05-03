import hashlib
from .all_query import query

un = 'aq_admin'
pw = 'aq_Password01!'
def hash_input(input_str):
    """
    HELPER FUNCTION
    take a manually entered string value
    RETURN its hash value (MD5)
    """
    return (hashlib.md5(input_str.encode())).hexdigest().encode()


def verify_user(*arg):
    """
    arg = [user name, password]
    RETURN a tuple of (table_name, password macheched) if login info is valid
    """
    table_list = ['aquarist', 'curator', 'event_manager', 'general_manager']
    sql_query = "SELECT hashed_pw FROM {} WHERE st_id = {};"
    q = query()

    with q.cursor(username = un, pwd = pw) as cur:
        for i in table_list:
            sql = sql_query.format(i, arg[0])
            cur.execute(sql)
            res = cur.fetchall()
            if res:
                if res[0][0] == hash_input(arg[1]):
                    return i, True
                else:
                    return i, False
    return "",False

if __name__ == '__main__':
    print(verify_user('123','123'))