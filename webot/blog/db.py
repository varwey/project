#filename:db.py
#encoding=utf8


import MySQLdb
import ConfigParser
import logging
import util




def GetMysqlConn():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read("/var/www/webot/blog/config.conf")
        db_host = cfg.get("db", "host")
        db_user = cfg.get("db", "user")
        db_passwd = cfg.get("db", "passwd")
        db_default = cfg.get("db", "default_db")

        conn = MySQLdb.connect(host=db_host,
                               user=db_user,
                               passwd=db_passwd,
                               db=db_default)
        conn.autocommit(True)
        conn.query("set names 'utf8'")

    except MySQLdb.MySQLError, e:
        util.getLogger().critical("error(%d:%s): connect"%(e.args[0], e.args[1]))
        return None

    return conn

def GetMysqlCursor():
    conn = cursor = None
    conn = GetMysqlConn()
    if conn is None:
        return None, None
    try:
        cursor = conn.cursor()
    except MySQLdb.MySQLError, e:
        util.getLogger().critical( "error(%d:%s): cursor()"%(e.args[0], e.args[1]))

    return conn, cursor

def tidy_str_for_mysql(str):
    if not isinstance(str, basestring):
        return str
    
    ret = str
    try:
        if str is not None and str != '':
            ret = str.replace('\\', '\\\\')
            str1 = ret
            ret = str1.replace('\'', r'\'')
    except:
        print "except: tidy_str_for_mysql, str=%s\n"%str
        return str
    else:
        return ret


