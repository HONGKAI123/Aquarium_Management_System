from sympy import arg
from all_query import query


# select
def select_example(*args):
    # 实例化 db connection API
    q = query()

    # 创建语句
    sql_query = "select * from {};".format(args[0])

    # 根据不同数据库登录信息执行
    with q.cursor(username = 'root', pwd = 'qweqwe123') as cur:
        cur.execute(sql_query)
        # 获得返回结果
        res = cur.fetchall()

    # 返回 结果和对应的名称
    return ['list', 'all', 'column', 'name', 'from', '*'], res






# select
def select_example(*args):
    # 实例化 db connection API
    q = query()

    # 创建语句
    sql_query ="SELECT curator FROM animal WHERE an_ID = '{}';".format(arg[0])
    query2 = "\
    SELECT fa_ID, f.name \
    FROM facility f \
    left join animal on f.fa_id = animal.habitat \
    where species = '{}' or (f.fa_ID not in (select habitat from animal group by habitat) and f.fa_ID not in (select e.facility from event e group by e.facility)) \
    group by fa_ID;".format(arg[0])
    # 根据不同数据库登录信息执行
    with q.cursor(username = 'root', pwd = 'qweqwe123') as cur:
        cur.execute(sql_query)
        # 获得返回结果
        res = cur.fetchall()

    # 返回 结果和对应的名称
    return ['list', 'all', 'column', 'name', 'from', '*'], res


#Add new animals
def insert_example(*args):
    # 实例化 db connection API
    q = query()

    # 创建语句
    sql_query = "\
    INSERT INTO animal VALUES ('{}','{}','{}', 0, '{}','{}');".format(arg[0], 
      arg[1],arg[2],arg[3],arg[4])


    # 根据不同数据库登录信息执行
    with q.cursor(username = 'root', pwd = 'qweqwe123') as cur:
        cur.execute(sql_query)

        # 提交修改后的语句到数据库
        q.conn.commit()

        # 获取被修改的行数
        res = cur.rowcount

    # 是否有任何数据被修改
    return True if res > 0 else False













# update
def update_example(*args):
    # 实例化 db connection API
    q = query()

    # 创建语句
    sql_query = "UPDATE animal \
    SET status = true \
    WHERE an_ID = {};".format(args[0])

    # 根据不同数据库登录信息执行
    with q.cursor(username = 'root', pwd = 'qweqwe123') as cur:
        cur.execute(sql_query)

        # 提交修改后的语句到数据库
        q.conn.commit()

        # 获取被修改的行数
        res = cur.rowcount

    # 是否有任何数据被修改
    return True if res > 0 else False


# insert
def insert_example(*args):
    # 实例化 db connection API
    q = query()

    # 创建语句
    sql_query = "INSERT INTO animal  \
                VALUES ('{}','{}','{}', 0, '{}','{}'); ".format(args[0],args[1],args[2],args[3],args[4])


    # 根据不同数据库登录信息执行
    with q.cursor(username = 'root', pwd = 'qweqwe123') as cur:
        cur.execute(sql_query)

        # 提交修改后的语句到数据库
        q.conn.commit()

        # 获取被修改的行数
        res = cur.rowcount

    # 是否有任何数据被修改
    return True if res > 0 else False


# delete
def delete_example(*args):
    # 实例化 db connection API
    q = query()

    # 创建语句
    sql_query = "DELETE FROM animal \
        WHERE an_ID = '{}';".format(args[0])


    # 根据不同数据库登录信息执行
    with q.cursor(username = 'root', pwd = 'qweqwe123') as cur:
        cur.execute(sql_query)

        # 提交修改后的语句到数据库
        q.conn.commit()

        # 获取被修改的行数
        res = cur.rowcount

    # 是否有任何数据被修改
    return True if res > 0 else False


if __name__ == '__main__':
    table_name = ['animal']
    data_from_select = select_example(*table_name)
    print(data_from_select)

    update_value = [101001]
    update_result = update_example(*update_value)
    print(update_result)

    # [an_ID, name, species, curator,habitat]
    insert_value = ['123456', 'hongkai', 'human', '736289249', '100005']
    insert_result = insert_example(*insert_value)
    print(insert_result)

    delete_value = ['123456']
    delete_result = delete_example(*delete_value)
    print(delete_result)