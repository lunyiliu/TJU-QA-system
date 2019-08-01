# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 11:25:10 2019

@author: lenovvo
"""

#输入: food,place,store,keyword（如果store不为空，则默认是模型把地点当做了store）
#（1）先根据place和store确定要推的店的大致范围
#(2)如果有特定的food，检查这家店关于该food的评论
#先不考虑food好了
#(3)按逗号分隔检查keywords,返回相关的评论,只取正向评论
#返回store,comment,keyword,ispositive,ispuzzled
import sys
from snownlp import SnowNLP
import jieba
import re
import pandas as pd
import pymysql
from random import sample
from random import choice
from menus import get_most_similar_stores_of_the_menus
conn = pymysql.connect(host='localhost', user='root', passwd='root', db='smart_qa', charset='utf8')
cursor=conn.cursor()
sys.path.append(r'C:\Users\lenovvo\Desktop\吴偶教授\天津大学智能问答\天大美食智能问答\gensim_菜单')
'''
not_patterns = [r"(不好|不要|不喜欢|拒绝|木|不|差|贵|脏|乱)",
                    r'([\u4e00-\u9fa5g]{1,4})(腻了|吃过|够了|多了|太|真是|垃圾)',
                    r'(不|没|无|拒绝|木|不想|受够了|讨厌)([\u4e00-\u9fa5g]{,4})']
'''
def ask_about_store(food,place_category,store_category,keywords):
    stores=[]
    if place_category or store_category:
        condition_column=place_category+store_category
        sql="select 店名,菜品 from meituan_overall where "
        if len(condition_column) >1:
            for condition in condition_column:
                sql+="地区='%s' or "%condition
            sql=sql[:-3]
        else:
            sql+="地区='%s' "%condition_column[0]
        cursor.execute(sql)
        conn.commit()
        data=cursor.fetchall()
        stores+=[Tuple[0] for Tuple in data]
    if store_category==[] and place_category==[]:
        sql="select 店名,菜品 from meituan_overall "
        cursor.execute(sql)
        conn.commit()
        data=cursor.fetchall()
        stores+=[Tuple[0] for Tuple in data]
    if keywords==[] and  food==[]:
        return choice(stores),[],[],True,False
    #如果有食物，不考虑关键词了
    if food:
        store=get_most_similar_stores_of_the_menus(food[0])
        return store,[],[],True,False
    #print( keywords)
    if len(stores)>200:
        stores=sample(stores,200)
    sql_detail="select 商店名称,详细菜品,评论 from meituan_detail where "
    for store in stores:
        sql_detail+="商店名称=\"%s\" or "%store
    sql_detail=sql_detail[:-3]
    #print(sql_detail)    
    cursor.execute(sql_detail)
    conn.commit()
    result=pd.DataFrame(list(cursor.fetchall()),columns=['商店名称','详细菜品','评论'])
    for i in range(len(result)):
        cuisine=[]
        dish_str=result.loc[i,'详细菜品']
        strs=dish_str.split(',')
        for Str in strs:
            if not re.search('[0-9]',Str):
                cuisine.append(Str)
        result.loc[i,'详细菜品']=cuisine
        comment_str=result.loc[i,'评论']
        if comment_str==None:
            comment_str=''
        result.loc[i,'评论']=re.split(',|。|!|！|，|;| ',comment_str)
    keyword=''
    for key in keywords:
        keyword+=key
    words=jieba.lcut_for_search(keyword)
    print(words)
    #添加一层过滤
    for word in words:
        if word=='呢' or word=='吧' or word=='好' or word=='的' or word=='有' or word=='是' or word =='或' or word =='多' or word =='情况'or word =='一点' or word =='高':
            words.remove(word)
    for i in range(len(result)):
        matched_comments=[]
        for word in words:
            for comment in result.loc[i,'评论']:
                if word in comment:
                    matched_comments.append(comment)
        if matched_comments==[]:
            continue
        else:
            sentiment_scores=[]
            for comment in matched_comments:
                s=SnowNLP(comment)
                score=s.sentiments
                sentiment_scores.append(score)
            #score_abs=[abs(score-0.5) for score in sentiment_scores]
            #print(matched_comments)
            index_returned=sentiment_scores.index(max(sentiment_scores))
            score_returned=sentiment_scores[index_returned]
            #错误判断的情感正负过滤
            if '干净' in matched_comments[index_returned] or '便宜'  in matched_comments[index_returned]:
                score_returned=0.9
                
            if  '绊脚石' in matched_comments[index_returned]  or '算了' in matched_comments[index_returned]  or '不存在' in matched_comments[index_returned] or '烦' in matched_comments[index_returned]  or '贵' in matched_comments[index_returned]  or '不便宜' in matched_comments[index_returned] or '价格高' in matched_comments[index_returned]:
                score_returned=0.1
            #print(score_returned)

            if score_returned > 0.5:
                return result.loc[i,'商店名称'],matched_comments[index_returned],word,True,False
    return [],[],[],True,True       
        
            