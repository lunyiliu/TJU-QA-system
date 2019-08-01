# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 15:27:55 2018

@author: Administrator
"""
from random import choice,sample
import pymysql;
from DBUtils.PooledDB import PooledDB;

import DB_config as Config;

pooled = PooledDB(creator=pymysql, mincached=Config.DB_MIN_CACHED , maxcached=Config.DB_MAX_CACHED, 
                                   maxshared=Config.DB_MAX_SHARED, maxconnections=Config.DB_MAX_CONNECYIONS, 
                                   blocking=Config.DB_BLOCKING, maxusage=Config.DB_MAX_USAGE, 
                                   setsession=Config.DB_SET_SESSION,
                                   host=Config.DB_TEST_HOST , port=Config.DB_TEST_PORT , 
                                   user=Config.DB_TEST_USER , passwd=Config.DB_TEST_PASSWORD ,
                                   db=Config.DB_TEST_DBNAME , use_unicode=True, charset=Config.DB_CHARSET);

                
conn=pooled.connection()
cur = conn.cursor()
menuNum = cur.execute("select * from oc_ai_product")
cur.close()
def unrepeat(tag_list):
    result=[]
    for i in range(1,7):
        string=''
        flag=0
        for n,s in enumerate(tag_list):
            if s[1]==i and flag==0:
               string=string+s[0]
               flag=1
            elif s[1]==i and flag==1:
               string=string+';'+s[0] 
        if string!='':
            result.append(string)
        else:
            result.append('其他')
    return result

def getMenuFeature(name):
    cur = conn.cursor()
    cur.execute("SELECT tag_name,category_id FROM oc_ai_product_tag WHERE id in(SELECT product_tag_id FROM oc_r_product_tag WHERE product_id ='%s');" %(name))
    cur.rowcount  
    get_row = list(cur.fetchall())
    get_row.sort(key=lambda x:x[1])
    cur.close()
    get_row=unrepeat(get_row)
    return get_row


        
def getQuestion(ids):
    cur = conn.cursor()
    cur.execute("SELECT cate_id,question FROM oc_ai_question WHERE id  =%d;" %(ids))
    cur.rowcount  
    get_row = cur.fetchall()
    cur.close()
    return list(get_row[0])

def getCataQuestion(cate):
    cur = conn.cursor()
    cur.execute("SELECT question FROM oc_ai_question WHERE cate_id  =%d;" %(cate))
    cur.rowcount  
    get_row = cur.fetchall()
    cur.close()
    listQUE = []
    for i in get_row:
        listQUE.append(i[0])
        
    return choice(listQUE)

def getIDQuestion(cate):
    cur = conn.cursor()
    cur.execute("SELECT id FROM oc_ai_question WHERE cate_id  =%d;" %(cate))
    cur.rowcount  
    get_row = cur.fetchall()
    cur.close()
    listQUE = []
    for i in get_row:
        listQUE.append(i[0])
        
    return choice(listQUE)

def getFood():
    cur = conn.cursor()
    cur.execute("SELECT tag_name FROM oc_ai_product_tag WHERE category_id  =2;")
    cur.rowcount  
    get_row = list(cur.fetchall())
#    print(get_row)
    cur.close()
    allList = []
    for i in get_row:
#        print(i[0])
        allList.extend(i[0].split('/'))
    return allList
#

def getMenuList(categoryId):
    cur = conn.cursor()
    cur.execute("SELECT product_id FROM oc_r_product_tag WHERE product_tag_id = %d;" %(categoryId))
    cur.rowcount  
    get_row = list(cur.fetchall())
#    print(get_row)
    cur.close()
    allList = []
    for i in get_row:
        allList.append(i[0])
    return allList


def getMenuName(ID):
    cur = conn.cursor()
    cur.execute("SELECT view_name FROM oc_ai_product WHERE id = %d;" %(ID))
    cur.rowcount  
    get_row = list(cur.fetchall())
#    print(get_row)
    cur.close()
    return get_row[0][0]


def getFirstFood():
    cur = conn.cursor()
    cur.execute("SELECT tag_name FROM oc_ai_product_tag WHERE category_id  =2;")
    cur.rowcount  
    get_row = list(cur.fetchall())
#    print(get_row)
    cur.close()
    allList = []
    for i in get_row:
#        print(i[0])
        allList.append(i[0].split('/'))
    return allList


def searchFood(string):
    cur = conn.cursor()
    cur.execute("SELECT reply FROM oc_ai_keyword_reply WHERE keyword = '%s';" %(string))
    cur.rowcount  
    get_row = list(cur.fetchall())
    allList = []
    for i in get_row:
        allList.append(i[0])
    return choice(allList)


def linkMap(foodList):
    stringList = []
    allList = getFirstFood()
    if len(foodList)>3 or len(foodList)==0:
        return ''
    try:
        for food in foodList:
            for lib in allList:
                if food in lib:
                    search = lib[0]
            stringList.append(searchFood(search))
    #    string = '<br/>'.join(stringList)    
        result =  choice(stringList)
    except:
        result = ''
    return result


        
def AnswerIDMap(answer):
    cur = conn.cursor()
    cur.execute("SELECT full_name,view_name FROM oc_ai_product;")
    cur.rowcount  
    get_row = list(cur.fetchall())
    cur.close()
    menus = 0
    for i,row in enumerate(get_row):
        for ro in row:            
            if ro in answer:
                menus = i+1        
    return menus








