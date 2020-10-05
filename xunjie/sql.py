import sys,os
import pymssql as py

def pysql(sql_con):   #针对有汉子查询数据库
  #首先获取数据库连接
    conn=py.connect(host="127.0.0.1",user="sa",password="zmy@518518",database="XJ",charset = 'utf8')
    #连接固定格式
    cursor=conn.cursor()
    cursor.execute('{}'.format(sql_con))
    py_con = cursor.fetchall()
    if not cursor:
        return 401
    else:
        return py_con
    conn.close()
def pysql_update(sql_con):
    #首先获取数据库连接

    conn = py.connect(host="127.0.0.1", user="sa", password="zmy@518518", database="XJ", charset='utf8')
    #连接固定格式
    cursor=conn.cursor()
    cursor.execute('{}'.format(sql_con))
    conn.commit()
    conn.close()
