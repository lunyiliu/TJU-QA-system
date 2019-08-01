# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 11:25:10 2019

@author: lenovvo
"""
#切记！！不要在循环里面改变被循环的变量
#关于"这家店"的处理,当做不存在
#输入: food,place,store,keyword
#（1）先根据place和store确定要关注的店的名称
#(2)如果有特定的food，检查这家店关于该food的评论
#先不考虑food好了
#(3)按逗号分隔检查keywords,返回相关的评论,判断正负
#返回store,comment,ispositive,ispuzzled
cheap_words=['便宜','物美价廉','价格低','打折','优惠','低价','甩卖','折扣','划算','实惠']
expensive_words=['贵','高价','天价','收费高','奢侈','奢华']
from snownlp import SnowNLP
import jieba
import re
import pandas as pd
import pymysql
from random import sample
conn = pymysql.connect(host='localhost', user='root', passwd='root', db='smart_qa', charset='utf8')
cursor=conn.cursor()
def ask_about_store_comment(food,place_category,store,keywords):
    NoStore=False
    if keywords==[] and food==[]:
        keywords.append('评价')
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
    if food:
        food+=keywords
        keywords=food
    if len(stores)>50:
        stores=sample(stores,50)
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
        if comment_str == None:
            comment_str = ''

        result.loc[i,'评论']=re.split(',|。|!|！|，|;| ',comment_str)
    keyword=''
    for key in keywords:
        keyword+=key
    #过滤纯粹的评价
    if '评价' in keyword or '评论' in keyword:
        if food==[]:
            for i in range(len(result)):
                for comment in result.loc[i,'评论']:
                    if comment:
                        s=SnowNLP(comment)
                        score=s.sentiments
                        if score > 0.9:
                            return '这家店',comment,True,False
                        if score <0.1:
                            return '这家店',comment,False,False
            return [],[],[],True  
        else:
            keyword=re.sub('评价|评论','',keyword)
    words=jieba.lcut_for_search(keyword)            
    words_counter=[]
    #添加一层过滤
    words_=[word for word in words]
    for word in words_:
        if word in cheap_words:
            words+=cheap_words
            words_counter=expensive_words
        if word in expensive_words:
            words+=expensive_words
            words_counter=cheap_words
        if word=='呢' or word=='吧' or word=='好' or word=='的' or word=='有' or word=='是' or word =='或' or word =='多' or word =='情况'or word =='一点':
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
            if '干净' in matched_comments[index_returned] or '便宜'  in matched_comments[index_returned] or '划算'  in matched_comments[index_returned]:
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

    if words_counter:
        print('counter_words found')
        for i in range(len(result)):
            counter_matched_comments=[]
            for word in words_counter:
                for comment in result.loc[i,'评论']:
                    if word in comment:
                        counter_matched_comments.append(comment)
            if counter_matched_comments==[]:
                continue
            else:
                sentiment_scores=[]
                for comment in counter_matched_comments:
                    s=SnowNLP(comment)
                    score=s.sentiments
                    sentiment_scores.append(score)
                score_abs=[abs(score-0.5) for score in sentiment_scores]
                #print(matched_comments)
                index_returned=score_abs.index(max(score_abs))
                score_returned=sentiment_scores[index_returned]
                #错误判断的情感正负过滤
                if '干净' in counter_matched_comments[index_returned] or '便宜'  in counter_matched_comments[index_returned] or '划算'  in counter_matched_comments[index_returned]:
                    score_returned=0.9
                    
                if  '烦' in counter_matched_comments[index_returned]  or '贵' in counter_matched_comments[index_returned]  or '不便宜' in counter_matched_comments[index_returned] or '价格高' in counter_matched_comments[index_returned]:
                    score_returned=0.1
                #print(score_returned)
                if not NoStore:
                    if score_returned > 0.5:
                        return result.loc[i,'商店名称'],counter_matched_comments[index_returned],True,False
                    if score_returned < 0.5:
                        return result.loc[i,'商店名称'],counter_matched_comments[index_returned],False,False
                else:
                    #这里要反向返回
                    if score_returned > 0.5:
                        return '这家店',counter_matched_comments[index_returned],True,False
                    if score_returned < 0.5:
                        return '这家店',counter_matched_comments[index_returned],False,False        
    return [],[],[],True       
        
            