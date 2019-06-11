# -*- coding: utf-8 -*-
"""
Created on Fri May 31 11:48:54 2019

@author: lenovvo
"""
#注意，输入店名请不要加括号
adj_pattern=r"(高|便宜|差|低|不|贵|脏|乱)"
import re
SENTENCE_CATE_ROOT=r'C:\Users\lenovvo\Desktop\吴偶教授\天津大学智能问答\天大美食智能问答\gensim_句子分类'
PLACE_ROOT=r'C:\Users\lenovvo\Desktop\吴偶教授\天津大学智能问答\天大美食智能问答\gensim_食品_地点_店家归类\地点'
FOOD_ROOT=r'C:\Users\lenovvo\Desktop\吴偶教授\天津大学智能问答\天大美食智能问答\gensim_食品_地点_店家归类\食品'
STORE_ROOT=r'C:\Users\lenovvo\Desktop\吴偶教授\天津大学智能问答\天大美食智能问答\gensim_食品_地点_店家归类\店家'
NER_ROOT=r'C:\Users\lenovvo\Desktop\吴偶教授\天津大学智能问答\天大美食智能问答\NER模型'
import sys
sys.path.append(NER_ROOT)
sys.path.append(PLACE_ROOT)
sys.path.append(FOOD_ROOT)
sys.path.append(STORE_ROOT)
sys.path.append(SENTENCE_CATE_ROOT)
from exmenu import predict
from stores import get_most_similar_stores
from dishes import get_most_similar_categ_of_the_dish
from places import get_most_similar_area_of_the_place
from question_type import get_most_similar_type_of_the_quetion
from 询问菜品 import ask_about_dishes
from 询问店评价 import ask_about_store_comment
from 询问店 import ask_about_store
synonym_dict={
        '饭馆':'店',
        '饭店':'店',
        '菜馆':'店',
        '酒店':'店'
        }
def replace_with_token(input_str,foods,places,stores):
    for food in foods:
        if food !='':
            input_str=input_str.replace(food,'S')
    for place in places:
        if place !='':
            input_str=input_str.replace(place,'D')
    for store in stores:
        if store !='':
            input_str=input_str.replace(store,'J')
    return input_str
def normalize_store(stores):
    store_category=[]
    if stores !=[]:
        #food_category=[get_most_similar_categ_of_the_dish(food) for food in foods]
        for store in stores:
            store_category.append(get_most_similar_stores(store))
    return store_category    
def normalize_food_place(foods,places):
    food_category=[]
    if foods !=[]:
        #food_category=[get_most_similar_categ_of_the_dish(food) for food in foods]
        for food in foods:
            food_categ=get_most_similar_categ_of_the_dish(food)
            for categ in food_categ:
                food_category.append(categ)
    if places !=[]:
        place_category=[get_most_similar_area_of_the_place(place) for place in places]
    else:
        place_category=[]
    return food_category,place_category
def handle_question(input_str):
     for key in synonym_dict.keys():
         input_str=input_str.replace(key,synonym_dict[key])
     food_str,place_str,store_str,keyword_str=predict(input_str)
     if food_str!='':
         foods=food_str.split(',')
     else:
         foods=[]
     if place_str!='':        
         places=place_str.split(',')
     else:
         places=[]
     if store_str!='':
         stores=store_str.split(',')
     else:
         stores=[]
     if keyword_str!='':
         keywords=keyword_str.split(',')
     else:
         keywords=[]
     token_str=replace_with_token(input_str,foods,places,stores)
     type_=get_most_similar_type_of_the_quetion(token_str)
     print(token_str+','+type_)
     if type_=='询问菜品':
         food_category,place_category=normalize_food_place(foods,places)
         dishes,isstore=ask_about_dishes(food_category,place_category,stores,keywords)
         if not isstore:
             reply='可以试试这几道哦,'
             for dish in dishes:
                 reply+='%s,'%dish
             reply=reply.strip(',')
         else:
             reply='可以试试%s这家的东西哦'%dishes
         if keywords:
             reply+=',挺%s'%keywords[0]
         return reply
     if type_=='询问店评价':
         food_category,place_category=normalize_food_place(foods,places)
         stores=normalize_store(stores)
         store_matched,comment_matched,ispositive,isempty=ask_about_store_comment(food_category,place_category,stores,keywords)
         if isempty:
             reply='抱歉,好像没有'
             if stores:
                 reply+='在%s'%stores[0]
             if place_category:
                 if not stores:
                     reply+='在%s'%places[0]
                 else:
                     reply+='和%s'%places[0]
             reply+='找到关于%s的信息~'%keywords[0]
         else:
             #过滤keywords
             keywords[0]=re.sub(adj_pattern,'',keywords[0])
             if place_category:
                 reply='%s的'%places[0]
             else:
                 reply=''
             reply+=store_matched+'在%s方面'%keywords[0]
             if ispositive:
                 reply+='还不错哦,'
             else:
                 reply+='好像一般呢,'
             reply+="有人说,'%s'"%comment_matched
         return reply
     if type_=='询问店':
         food_category,place_category=normalize_food_place(foods,places)
         food_category,store_category=normalize_food_place(foods,stores)
         store_matched,comment_matched,ispositive,isempty=ask_about_store(food_category,place_category,store_category,keywords)
         if isempty:
             reply='抱歉,好像没有'
             if store_category:
                 reply+='在%s'%stores[0]
             if place_category:
                 if not store_category:
                     reply+='在%s'%places[0]
                 else:
                     reply+='和%s'%places[0]
             reply+='找到这样的店哦~'
         else:
             #过滤keywords
             keywords[0]=re.sub(adj_pattern,'',keywords[0])
             reply='如果考虑%s的话,可以试试%s哦,'%(keywords[0],store_matched)
             reply+="有人说,'%s'"%comment_matched
         return reply
             
     return []