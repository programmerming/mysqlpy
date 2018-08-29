mysqldump_command_dict = {
        'dumpcommand':'mysqldump',
        'server':'192.168.10.6',
        'port':3306,
        'user':'',
        'password':'',
        'db':''
        }

conn_dict = {
        'host':'192.168.10.6',
        'port':3306,
        'user':'',
        'password':'',
        'db':'',
        'charset':'utf8'
        }

target_dict = {
        'host':'192.168.10.6',
        'port':3306,
        'user':'',
        'password':'',
        'db':'',
        'charset':'utf8'
        }

sql_getTables = "select table_name from information_schema.`TABLES` WHERE TABLE_SCHEMA='%s';"
sql_getColumns = "select column_name,column_type from information_schema.`COLUMNS` WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s';"
sql_showCreate = "show create TABLE %s;"


mysql_file_path = ".\mysqlscriptData"