#-*- coding: utf-8 -*-
import os
import pymysql
import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import Config

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

def dbNotPlayerData():
    conn = DBTool(Config.conn_dict)
    li = conn.execute_query(Config.sql_getTables)
    
    mysqldump_command_dict = Config.mysqldump_command_dict
    
    if list:
        pTables = ""
        sTables = ""
        for row in li:
            #表名
            dbtable = row[0]
            if str(dbtable).startswith('p_'):
                if len(pTables) <=0:
                    pTables = dbtable
                else:
                    pTables = pTables + " " + dbtable
            elif str(dbtable).startswith('sys_'):
                if len(sTables) <=0:
                    sTables = dbtable
                else:
                    sTables = sTables + " " + dbtable
            else:
                continue
        sqlfromat = "%s --no-defaults --no-data %s -h%s -u%s -p%s -P%s %s %s > %s"
        sql = (sqlfromat % (mysqldump_command_dict['dumpcommand'],
                                '--no-data',
                                mysqldump_command_dict['server'],
                                mysqldump_command_dict['user'],
                                mysqldump_command_dict['password'],
                                mysqldump_command_dict['port'],
                                mysqldump_command_dict['db'],
                                pTables,
                                "playerDataStruct.sql"))
        print(sql)
        result = os.system(sql)
        if not result:
            print("export playerDataStruct Success!")
        else:
            print("export playerDataStruct Fail!")
        sqlfromat = "%s --no-defaults -h%s -u%s -p%s -P%s %s %s > %s"
        sql = (sqlfromat % (mysqldump_command_dict['dumpcommand'],
                                mysqldump_command_dict['server'],
                                mysqldump_command_dict['user'],
                                mysqldump_command_dict['password'],
                                mysqldump_command_dict['port'],
                                mysqldump_command_dict['db'],
                                sTables,
                                "sysData.sql"))
        print(sql)
        result = os.system(sql)
        if not result:
            print("export sysData Success!")
        else:
            print("export sysData Fail!")
            
def db():
    mysqldump_command_dict = Config.mysqldump_command_dict
    sqlformat = "%s --no-defaults -h%s -u%s -p%s -P%s %s > %s"
    sql = (sqlformat % (mysqldump_command_dict['dumpcommand'],
                                mysqldump_command_dict['server'],
                                mysqldump_command_dict['user'],
                                mysqldump_command_dict['password'],
                                mysqldump_command_dict['port'],
                                mysqldump_command_dict['db'],
                                "data.sql"))
    print(sql)
    result = os.system(sql)
    if not result:
        print "export all data Success!"
    else:
        print "export all data Fail!"
    return

def dbDiff():
    fo = open("diff.sql","w+")
    
    sDBName = Config.conn_dict['db']
    tDBName = Config.target_dict['db']
    
    sc = DBTool(Config.conn_dict)
    sTables = sc.execute_query(Config.sql_getTables % sDBName)
    tc = DBTool(Config.target_dict)
    tTables = tc.execute_query(Config.sql_getTables % tDBName)
    
    #当前新增的数据库表
    for row in sTables:
        tableName = row[0]
        if not str(tableName).startswith('p_'):
            continue
        if row not in tTables:
            sc = DBTool(Config.conn_dict)
            create = sc.execute_query(Config.sql_showCreate % row[0])
            fo.write(str(create[0][1]))
            fo.write(";\n\r")
            
    #当前删除的数据表
    deleteTables = ()
    for row in tTables:
        tableName = row[0]
        if not str(tableName).startswith('p_'):
            continue
        if row not in sTables:
            deleteTables = deleteTables+row
            fo.write("DROP TABLE %s" % row[0])
    
    columnsSql = Config.sql_getColumns
    #遍历共同拥有的表，处理表结构
    for row in tTables:
        if not str(row[0]).startswith('p_'):
            continue
        if row in deleteTables:
            continue
        sc = DBTool(Config.conn_dict)
        sColumns = sc.execute_query(columnsSql % (sDBName,row[0]))
        tc = DBTool(Config.target_dict)
        tColumns = tc.execute_query(columnsSql % (tDBName,row[0]))
        for column in tColumns:
            if column not in sColumns:
                fo.write("ALTER TABLE %s drop %s;\n" % (row[0],column[0]))
        for column in sColumns:
            if column not in tColumns:
                fo.write("ALTER TABLE %s add %s %s;\n" % (row[0],column[0],column[1]))
    fo.close()
            
def generate():
    if not os.path.exists(Config.mysql_file_path):
        os.mkdir(Config.mysql_file_path)
        
    os.chdir(Config.mysql_file_path)
    
    while True:
        print "========================================================="
        print "输入0：退出"
        print "输入1：导出数据库数据备份"
        print "输入2：导出玩家数据表结构和配置数据表结构及数据"
        print "输入3：导出数据库与目标数据库的差异操作"
        
        print "========================================================="
    
        text = raw_input("")
        print
        if text == "0":
            print "退出"
            return
        elif text == "1":
            db()
            return
        elif text == "2":
            dbNotPlayerData()
            return
        elif text == "3":
            dbDiff()
            return
        else:
            print "非法输入"
            
        print "\n\n"
    
if __name__ == '__main__':
    try:
        generate()
    except:
        traceback.print_exc()
         
    print
    os.system("pause")
        