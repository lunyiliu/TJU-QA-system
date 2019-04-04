'''
middle 在第一个问题作为未识别菜谱标志
其余问题作为中间推荐标识
'''

from robot_food_one import robot_que_food
from robot_cuisine_two import robot_que_cuisine
from robot_taste_three import robot_que_taste
from robot_degree_four import robot_que_degree
from robot_cool_five import robot_que_cool
from robot_health_six import robot_que_health
from robot_alone_seven import robot_que_alone
from robot_photo_eight import robot_que_photo
from menuSql import getQuestion
from utils import matchGrooves
import numpy as np
from langconv import Converter


# 转换繁体到简体
def cht_to_chs(line):
    line = Converter('zh-hans').convert(line)
    line.encode('utf-8')
    return line


userID = 111
sessionID = 111
answerID = 0
answer = '豆角'
flag = 0
repeatNum = 0
questionID = 1
questionLists = [1,2,3,4,5,6,7]
Groove = ['',0,0,0,0,0,0,0]
middle = ''


def oc_tju_robot(user_id, answer_id, sessionID,
                 answer, flag, repeatNum, middle,
                 questionID, questionLists, Groove):


    answerTag = '测试1,测试2'
    emotionScore = 0.5
    unknowFlag = 0
    menuLists = []
    answer = cht_to_chs(answer)
    categoryID, categoryquestion= getQuestion(questionID)
    if categoryID==1:

        isPass,flag,repeatNum,question,nextQuestion,questionFilter,Groove,menuLists,middle,unknowFlag \
        = robot_que_food(answer,flag, repeatNum, categoryID, questionLists,middle ,Groove)

    elif categoryID==2:
        isPass,flag,repeatNum,question,nextQuestion,questionFilter,Groove,menuLists,middle,unknowFlag \
        = robot_que_cuisine(answer,flag, repeatNum, categoryID, questionLists,middle ,Groove)

    elif categoryID==3:
        isPass,flag,repeatNum,question,nextQuestion,questionFilter,Groove,menuLists ,middle,unknowFlag\
        = robot_que_taste(answer,flag, repeatNum, categoryID, questionLists,middle, Groove)

    elif categoryID==4:
        isPass,flag,repeatNum,question,nextQuestion,questionFilter,Groove,menuLists ,middle,unknowFlag\
        = robot_que_degree(answer,flag, repeatNum, categoryID, questionLists,middle ,Groove)

    elif categoryID == 5:
        flag, isPass, repeatNum, question, nextQuestion, questionFilter, Groove, menuLists, middle, unknowFlag \
        = robot_que_cool(answer,flag, repeatNum, categoryID, questionLists ,middle,Groove)

    elif categoryID==6:
        isPass,flag,repeatNum,question,nextQuestion,questionFilter,Groove,menuLists,middle,unknowFlag \
        = robot_que_health(answer,flag, repeatNum, categoryID, questionLists,middle, Groove)

    elif categoryID==7:
        isPass,flag,repeatNum,question,nextQuestion,questionFilter,Groove,menuLists,middle,unknowFlag \
        = robot_que_alone(answer,flag, repeatNum, categoryID, questionLists,middle, Groove)

    elif categoryID==8:
        isPass,flag,repeatNum,question,nextQuestion,questionFilter,Groove,menuLists,middle,unknowFlag \
        = robot_que_photo(answer,flag, repeatNum, categoryID, questionLists,middle, Groove)

    elif categoryID==9:
        isPass,flag,repeatNum,question,nextQuestion,questionFilter,Groove,menuLists ,middle,unknowFlag\
        = robot_que_photo(answer,flag, repeatNum, categoryID, questionLists,middle, Groove)



    if isPass==1:  
        #该轮对话通过则answer_id
        answer_id+=1
        if answer_id==4 or Groove.count(0)==4:
            #并且判断是否可以推荐菜谱了
            menuLists = matchGrooves(Groove)
            isPass = 3
            question = '为您推荐了以下菜谱。'

    return [user_id, sessionID, answer_id, answerTag, emotionScore, menuLists, middle, unknowFlag, \
            isPass, flag, repeatNum, question, nextQuestion, questionFilter, Groove]