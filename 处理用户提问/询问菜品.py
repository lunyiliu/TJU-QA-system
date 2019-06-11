# -*- coding: utf-8 -*-
"""
Created on Tue May 28 08:13:33 2019

@author: lenovvo
"""
'''
先按地点和店名进行粗筛，取出符合的所有菜名，
再对每个菜名按菜品种类和关键词进行筛选
'''
'''
2019.5.29
今天解决了一个神奇的BUG
gensim 模型里面，在初次训练对象时，similarities对象最后会存储在相对路径里，连带着shard对象也存在了和
similarities对象的一个路径里。。
我现在在另一个路径里导入gensim，此时由于相对路径变了，因此我必须从绝对路径读取similarities对象文件，
然而读取shard对象的路径依然是初次训练对象时的绝对路径，原因是shard对象的路径在模型里是不变的，没有外接口。
理论上来说我只需要在当前的绝对路径下重新训练gensim模型就好了，这样shard对象会变成绝对路径，
但是这样就报错了，而且我看不懂
所以我只能修改gensim包，更新shard对象的读取路径为绝对路径
'''
from random import sample
import re
from random import choice
import sys
sys.path.append(r'C:\Users\lenovvo\Desktop\吴偶教授\天津大学智能问答\天大美食智能问答\gensim_食品_地点_店家归类\店家')
sys.path.append(r'C:\Users\lenovvo\Desktop\吴偶教授\天津大学智能问答\天大美食智能问答\gensim_评论')
sys.path.append(r'C:\Users\lenovvo\Desktop\吴偶教授\天津大学智能问答\天大美食智能问答\gensim_食品_地点_店家归类\食品')
import jieba
from stores import get_most_similar_stores
from comments import get_most_similar_stores_of_the_keyword
import pymysql
conn = pymysql.connect(host='39.97.100.184', user='root', passwd='8612260', db='smart_qa', charset='utf8')
cursor=conn.cursor()
#DBh=DB_handler()
def ask_about_dishes(food_category,place_category,stores,keywords)->'所有的参数都是列表,return: result,isStore':
    sql="select 店名 from meituan_overall "
    if  place_category!=[] or  food_category !=[]:
        sql+='where '
    if place_category:
        if len(place_category) >1:
            for place in place_category:
                sql+="地区='%s' or "%place
            sql=sql[:-3]
        else:
            sql+="地区='%s' "%place_category[0]
    if food_category:
        if place_category:
            sql+='and '
        if len(food_category) >1:
            for food in food_category:
                sql+="菜品种类='%s' or "%food
            sql=sql[:-3]
        else:
            sql+="菜品种类='%s' "%food_category[0]  
    #print(sql)
    cursor.execute(sql)
    conn.commit()
    store_names=[Tuple[0] for Tuple in cursor.fetchall()]     
    if stores:
        store_names=[]
        for store in stores:
            store_names.append(get_most_similar_stores(store))
    
    if len(store_names)>50:
        store_names=sample(store_names,50)
    #print(store_names)
    assert(store_names != [])
    #取出符合条件的所有菜名和详细评论
    sql_detail="select 详细菜品,评论 from meituan_detail where "
    for store in store_names:
        sql_detail+="商店名称=\"%s\" or "%store
    sql_detail=sql_detail[:-3]
    #print(sql_detail)    
    cursor.execute(sql_detail)
    conn.commit()
    result=cursor.fetchall()
    #print(len(result))
    cuisine=[] 
    keywords=keywords+food_category
    
    if  keywords ==[]:
        dish_str=choice(result)[0]     
        strs=dish_str.split(',')
        for Str in strs:
            if not re.search('[0-9]',Str):
                cuisine.append(Str)
        if len(cuisine)>2:
            return sample(cuisine,3),False
        else:
            return cuisine  ,False
    else:
        keyword=[]
        for kw in keywords:
            keyword+=jieba.lcut_for_search(kw)
        dish_strs=''
        for row in result:
            dish_strs+=row[0]
            dish_strs+=','
        strs=dish_strs.split(',')
        for Str in strs:
            if not re.search('[0-9]',Str):
                cuisine.append(Str)
        #print(cuisine)
        matched_cuisine=[]
        for dish in cuisine:
            for key in keywords:
                if key in dish:
                    matched_cuisine.append(dish)
        #print(matched_cuisine)
        if matched_cuisine:
            if len(matched_cuisine)>2:
                return sample(matched_cuisine,3),False
            else:
                return matched_cuisine,False
        else:
            store=get_most_similar_stores_of_the_keyword("".join(keyword))
        return store,True
        '''
        strs=dish_str.split(',')
        for Str in strs:
            if not re.search('[0-9]',Str):
                matched_cuisine.append(Str)
        if len(matched_cuisine)>2:
            return sample(matched_cuisine,3)
        else:
            return matched_cuisine            
        '''
        '''
        for row in result:
            if keyword in row[0] or keyword in row[1]:
                dish_strs.append(row[0])
        '''                    
            
