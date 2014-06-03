#encoding=utf-8
'''
功能：从crontab记录中导入任务到mysql
创建日期：2013-09-13，作者：贺伟刚
'''

import util
import re
import db
import urllib2
import json,time
import MySQLdb

def get_info(task):
    '''
    从crontab中的一行，提取参数
    '''
    result_list = re.compile("project=(\w+)[\S\s]*spider=(\w+)[\S\s]+config=(\S+)\s*$").findall(task)
    if len(result_list) == 0:
        return "", "", "", ""
    else:
        project_name, spider_name, config_url =  result_list[0]
        category_name_list = re.compile("(mblog|blog|bbs|news|search)").findall(task)
        category_name = ""
        if len(category_name_list) >0:
            category_name = category_name_list[0]
        return  project_name, spider_name, config_url, category_name


def import_crontab(file_name, tag):    
    '''
        从旧版本的任务定时记录中，导入到mysql数据库
        参数：filename：要导入的cron文件名，需要放到和import_task.py同一目录
                 tag：用于标识本次导入的数据，会添加到mysql的tag字段
    '''
    fp = open(file_name)
        
    task_list = []
    conn = MySQLdb.connect()
    cursor = conn.cursor()
    
    count = 0
    for line in fp.readlines():
        
        if line[0] == '#' or len(line)<10:
            continue
        
        project_name, spider_name, config_url, category_name = get_info(line)
        #print "project_name:%s, spider_name:%s, config_url:%s"%(project_name, spider_name, config_url)
        
        try:
            json_str = urllib2.urlopen(config_url).read()
        except:
            print line
            continue
        
        config = json.loads(json_str)
        domain_name = config['site'].encode('utf-8')
        domain = config['domains'][0].encode('utf-8')
        
        now = time.time()
        sql = "insert ignore into task_list (category_name, domain, domain_name, config_url, project_name, spider_name, spider_params,  priority_seconds, create_datetime,update_datetime, tag) values(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', %d, %d,%d,\'%s\')"%(
                                    category_name,
                                    domain, 
                                    domain_name,
                                    config_url,
                                    project_name,
                                    spider_name,
                                    ' -s CONCURRENT_REQUESTS_PER_DOMAIN=100  -s CONCURRENT_REQUESTS=100 ',
                                    60,
                                     now,
                                     now,
                                     tag
                                     )
        #print sql
        cursor.execute(sql)
        count += 1
    cursor.close()
    conn.close()    
    print count

if __name__ == "__main__":
#     import_crontab("/crontab-test.txt", "test")        
#     import_crontab("/crontab-175.txt", "main")
    import_crontab("/crontab-168.txt", "tieba180")

    
    

    
