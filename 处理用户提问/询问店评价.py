# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 11:25:10 2019

@author: lenovvo
"""
#关于"这家店"的处理,当做不存在
#输入: food,place,store,keyword
#（1）先根据place和store确定要关注的店的名称
#(2)如果有特定的food，检查这家店关于该food的评论
#先不考虑food好了
#(3)按逗号分隔检查keywords,返回相关的评论,判断正负
#返回store,comment,ispositive,ispuzzled
from snownlp import SnowNLP
import jieba
import re
import pandas as pd
import pymysql
from random import sample
conn = pymysql.connect(host='39.97.100.184', user='root', passwd='8612260', db='smart_qa', charset='utf8')
cursor=conn.cursor()
'''
not_patterns = [r"(不好|不要|不喜欢|拒绝|木|不|差|贵|脏|乱)",
                    r'([\u4e00-\u9fa5g]{1,4})(腻了|吃过|够了|多了|太|真是|垃圾)',
                    r'(不|没|无|拒绝|木|不想|受够了|讨厌)([\u4e00-\u9fa5g]{,4})']
'''
def ask_about_store_comment(food,place_category,store,keywords):
    NoStore=False
    assert(keywords)
    stores=[]
    if store:
        stores=store
    if place_category:
        sql="select 店名 from meituan_overall where "
        if len(place_category) >1:
            for place in place_category:
                sql+="地区='%s' or "%place
            sql=sql[:-3]
        else:
            sql+="地区='%s' "%place_category[0]
        cursor.execute(sql)
        conn.commit()
        stores+=[Tuple[0] for Tuple in cursor.fetchall()]
    if store==[] and place_category==[]:
        sql="select 店名 from meituan_overall "
        cursor.execute(sql)
        conn.commit()
        stores+=[Tuple[0] for Tuple in cursor.fetchall()]
        NoStore=True
    if len(stores)>30:
        stores=sample(stores,30)
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
        result.loc[i,'评论']=re.split(',|。|!|！|，|;| ',comment_str)
    keyword=''
    for key in keywords:
        keyword+=key
    words=jieba.lcut_for_search(keyword)
    #添加一层过滤
    for word in words:
        if word=='好' or word=='的' or word=='有' or word=='是' or word =='或' or word =='多' or word =='情况':
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
            score_abs=[abs(score-0.5) for score in sentiment_scores]
            #print(matched_comments)
            index_returned=score_abs.index(max(score_abs))
            score_returned=sentiment_scores[index_returned]
            #错误判断的情感正负过滤
            if '干净' in matched_comments[index_returned] or '便宜'  in matched_comments[index_returned]:
                score_returned=0.9
                
            if  '烦' in matched_comments[index_returned]  or '贵' in matched_comments[index_returned]  or '不便宜' in matched_comments[index_returned] or '价格高' in matched_comments[index_returned]:
                score_returned=0.1
            #print(score_returned)
            if not NoStore:
                if score_returned > 0.5:
                    return result.loc[i,'商店名称'],matched_comments[index_returned],True,False
                if score_returned < 0.5:
                    return result.loc[i,'商店名称'],matched_comments[index_returned],False,False
            else:
                if score_returned > 0.5:
                    return '这家店',matched_comments[index_returned],True,False
                if score_returned < 0.5:
                    return '这家店',matched_comments[index_returned],False,False
    return [],[],[],True       
        
            