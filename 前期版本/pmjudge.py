# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 08:29:02 2019

@author: lenovo
"""
import re
import string

pm0 = re.compile(u'(没错|没问题|不错|没事|没有问题)')  # 有否定词但是是肯定
pm1 = re.compile(u'(不挑|没这必要|没这需|没这要|没那个要|没那个必|没这|没有要求|没要求|没太多要求|没这必要|没这个必要|没那个必要|没这个需要|没那个需要|没有要求|没有这个需求|没这个需求|没有太多要求|没有这必要|没有这个必要|没有那个必要|没有这个需要|没有那个需要)') # 有否定词但是是中性
pm2 = re.compile(u'(不|算了|别|拒绝|讨厌|恨|徒有其表|厌恶|烦|拉倒|no|不需要|不用|没必要|没啥用|不中用)') # 否定词
pm3 = re.compile(u'(都可以|都行|不挑|都想|随便|无所谓|都还行|随意|都阔以)') # 通
pm4 = re.compile(u'(需要|想要|希望有|最好有|可以|好|是|想|要|嗯|行|就这样|看看|ok|yes|必须|试试|来一台|喜欢|中意|阔以)') # 肯定
pm5 = re.compile(u'(想想|想一想|想一下|想下|说说)')
pm6 = re.compile(u'(有没有|带不带)')

pm_cl1 = re.compile(u'(面积|家用|办公室)')
pm_cl2 = re.compile(u'(霾|PM)')
pm_cl3 = re.compile(u'(你说呢|你猜|霾|空气|pm|除)')

#for the question of pm2.5
def pmjudgment1(answers): # [是，不是]
    answer = answers.lower()
    if answer == '除霾' or answer == '除啊' or answer == '除':
        return 1
    if re.search(pm5, answer):
        return 0
    elif re.search(pm0, answer):
        return 1
    elif re.search(pm1, answer):
        return 2
    elif re.search(pm2, answer) and answer.find('要不')==-1:
        if '区别' in answer:
            return 0
        return 2
    elif re.search(pm3, answer):
        return 3
    elif re.search(pm4, answer) and not re.search(pm_cl1, answer):
        return 1
    elif re.search(pm_cl3, answer):
        return 4
    else:
        return 0


#for other  questions
def pmjudgment02(answer):
    
    nPos1=int(answer.rfind('霾'))
    nPos2=int(answer.rfind('pm'))
    nPos = -1
    if nPos1 > 0:
        nPos = nPos1
    if nPos2 > 0:
        nPos = nPos2
    if nPos <= -1:
        return 0
    
    print(nPos)
    
    if re.search(pm6, answer[2:7]):
        return 4
    
    if re.search(pm4, answer[nPos-5:nPos+5]):
        return 1
    
    if re.search(pm1, answer[nPos-5:nPos+5]) or re.search(pm2, answer[nPos-5:nPos+5]):
        return 2  
    
    if re.search(pm3, answer[nPos-5:nPos+5]):
        return 3
      
    return 0


# qindex 1 表示除霾问题； 否则 其他
#返回
#0: 无关
#1：yes
#2: no
#3: both
#4：相关但不清楚
def pmjudgment(userstr, qindex):
    result = 0
    if qindex == 1:
        result = pmjudgment1(userstr)
    else:
        result = pmjudgment02(userstr)
    return result

 
#返回
#0: 无关
#1：yes
#2: no
#3: both
#4：相关但不清楚

if __name__=='__main__':
    teststr = '没有这个需求，一般的就行'
    #[numbers, lesslarger, isdisturb, isarea] = numberdetection(teststr)
    result = pmjudgment(teststr, 1)   
    if(result == 0):
        print('对不起你跑题了')
    if(result == 1):
        print('好的，我们有')
    if(result == 2):
        print('好的，可以没有')
    if(result == 3):
        print('好的，优先选不除霾的')
    if(result == 4):
        print('对不起，我蒙圈了')

    
    
    
    
    
    
    
    
    
    
    
    