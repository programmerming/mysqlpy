#-*- coding: utf-8 -*-
import os
import pymysql

class DBTool:
    
    conn = None
    cursor = None
    
    def __init__(self,conn_dict):
        self.conn = pymysql.connect(host=conn_dict['host'],
                                    port=conn_dict['port'],
                                    user=conn_dict['user'],
                                    passwd=conn_dict['password'],
                                    db=conn_dict['db'],
                                    charset=conn_dict['charset']
                                    )
        self.cursor = self.conn.cursor()
        
    def execute_query(self,sql_string):
        try:
            cur = self.cursor
            cur.execute(sql_string)
            li = cur.fetchall()
            cur.close()
            self.conn.close()
            return li
        except pymysql.Error as e:
            print("mysql execute error:",e)
            raise

    def execute_noquery(self,sql_string):
        try:
            cursor = self.cursor
            cursor.execute(sql_string)
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
        except pymysql.Error as e:
            print("mysql execute error:",e)
            raise

def main():
    conn_dict = {
        'host':'192.168.10.204',
        'port':3306,
        'user':'root',
        'password':'root',
        'db':'mdqk_game_dev',
        'charset':'utf8'
        }
    conn = DBTool(conn_dict)
    sql_getTables = "select table_name from information_schema.`TABLES` WHERE TABLE_SCHEMA='mdqk_game_dev';"
    li = conn.execute_query(sql_getTables)
    
    mysql_file_path = "..\msyqlscript"
    if not os.path.exists(mysql_file_path):
        os.mkdir(mysql_file_path)
    
    mysqldump_command_dict = {
        'dumpcommand':'mysqldump',
        'server':'192.168.10.204',
        'port':3306,
        'user':'root',
        'password':'root',
        'db':'mdqk_game_dev'
        }
    
    if list:
        for row in li:
            print(row[0])
            # 切换到新建的文件夹中
            os.chdir(mysql_file_path)
            #表名
            dbtable = row[0]
            #文件名
            exportfile = row[0] + '.sql'
            if str(dbtable).startswith('p_'):
                sqlfromat = "%s --no-defaults %s -h%s -u%s -p%s -P%s %s %s > %s"
                sql = (sqlfromat % (mysqldump_command_dict['dumpcommand'],
                                '--no-data',
                                mysqldump_command_dict['server'],
                                mysqldump_command_dict['user'],
                                mysqldump_command_dict['password'],
                                mysqldump_command_dict['port'],
                                mysqldump_command_dict['db'],
                                dbtable,
                                exportfile))
            elif str(dbtable).startswith('sys_'):
                sqlfromat = "%s --no-defaults -h%s -u%s -p%s -P%s %s %s > %s"
                sql = (sqlfromat % (mysqldump_command_dict['dumpcommand'],
                                mysqldump_command_dict['server'],
                                mysqldump_command_dict['user'],
                                mysqldump_command_dict['password'],
                                mysqldump_command_dict['port'],
                                mysqldump_command_dict['db'],
                                dbtable,
                                exportfile))
            else:
                continue
            print(sql)
            result = os.system(sql)
            if not result:
                print('export ok')
            else:
                print('export fail')
            
if __name__ == '__main__':
    main()