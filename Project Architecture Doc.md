# ~~API Doc~~

# Project Doc


## 总览

```mermaid
sequenceDiagram
participant Web/CLI
participant Mid Logic
participant Database
Web/CLI->>Mid Logic:各类参数
note left of Web/CLI:参数:current user,etc..
Mid Logic->>Database:根据参数执行指令
Database-->>Web/CLI:输出数据库结果
Database->>Mid Logic:返回数据库结果
Mid Logic->>Web/CLI:整理结果后输出
```

## Logic

```mermaid
flowchart LR
subgraph menu_d[可做成 menu]
direction LR
e_report[view events report]
%% new_event[create new event] 
s_report[view stff report]
end

subgraph menu_m[可做成 menu]
direction LR
e_single_report[view this person's event]
aquarist_check[check all aquarist availability]
facility_check[check all facility availability]
log_report
end

subgraph menu_c[可做成 menu]
check_animal[check all animals' status]
add_animal
end



login-->|检查用户是否存在,职位|main;
main-.->|Director|main_D;
main-.->|Manager|main_M;
main-.->|Curator|main_C;
main-.->|Aquarist|main_A;

main_D --- menu_d;
e_report-->e_show[all reports+add event as a choice]
e_report-->create_new_event[get input+flush event report]
s_report-->s_show[all reports+add hire/fire as choices]
s_report--->stuff_hire[hire stuff input+flush stuff report]
s_report--->stuff_fire[choose stuff+flush stuff report]

main_M --- menu_m;
e_single_report-->e_s_r_show[all relative reports]
aquarist_check-->ac[aquarist report+assign aquarist as a choice]
facility_check-->fc[facility report+assign facility as a choice]
log_report-->lr[edit as a choice]

main_C --- menu_c;
check_animal-->animal_edit[choose one to edit as a choice]
main_C-->facility_check

main_A --> vmc[view maintenance schedule+mantain as a choice];
vmc --> mantain[choose facility to clean ]



```





### 四大操作 增删改查

Director menu

| 增               | 删         | 改   | 查                 |
| ---- | ---- | ---- | ---- |
| Create new event | Fire staff | -    | View events report |
| Hire staff       | -          | -    | view staff report  |

Event Manager menu

| 增   | 删   | 改   | 查   |
| ---- | ---- | ---- | ---- |
|-|-|Assign aquarist to event|View your events|
|-|-|Assign facility to event|check aquarist availability|
|-|-|Log event attendance|check facility availability|

Curator menu function


| 增   | 删   | 改   | 查   |
| ---- | ---- | ---- | ---- |
|Add new animal|-|feed your animals|Check on your animals|
|-|-|-|check facility availability|

Aquarist menu

| 增   | 删   | 改                | 查                        |
| ---- | ---- | ---- | ---- |
| -    | -    | Maintain facility | View maintenance schedule |

----

## 数据库连接

驱动:

[mysqlclien](https://pypi.org/project/mysqlclient/)

Storage Engine:

[InnoDB](https://dev.mysql.com/doc/refman/8.0/en/innodb-storage-engine.html)

**基本流程**:

```mermaid
graph TD;
	Connect-->Disconnect;
	Connect-->Cursor;
	Cursor-->sql1[Execute SQL Query 1];
	sql1-->sql2[execute SQL Query2];
	sql2-->etc[more SQL...];
	etc-->Disconnect;
	
```



### pseudo code:

Django Setting:

```python
"""
Database Conf
"""
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '/path/to/my.cnf',
        },
    }
}


# my.cnf
[client]
database = NAME
user = USER
password = PASSWORD
default-character-set = utf8
```

Function Example:

```python
from django.db import connection
"""
连接数据库后
"""
def my_custom_sql(self):
    with connection.cursor() as cursor: 
    # with 关键词将在 该 func 运行完之后自动解除
    # 即 connect-> 执行语句->disconnect
        cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
        row = cursor.fetchone()
        # fetchone 抓取一条执行后的返回值
    return row
  
```

## API

### select

| Function name | input(format)                     | Output(format)              |
| ------------- | --------------------------------- | --------------------------- |
| login_account | Usernamd, password(string,string) | has any suitable value(T/F) |
|               |                                   |                             |
|               |                                   |                             |

- login_account

  根据已有用户名/密码查找是否存在该用户

  明文密码哈希转换后和数据库中比对

  

### insert

| Function name | input(format) | Output(format)       |
| ------------- | ------------- | -------------------- |
| new_event     | ???           | query seceeed? (T/F) |
|               |               | query seceeed? (T/F) |
|               |               | query seceeed? (T/F) |
|               |               | query seceeed? (T/F) |

- new_event

