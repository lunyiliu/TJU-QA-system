# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 08:29:02 2019

@author: lenovo
"""

import re
import string
s = '38x1x234x35x612x3yxxx'


CN_NUM = {
    '〇' : 0, '一' : 1, '二' : 2, '三' : 3, '四' : 4, '五' : 5, '六' : 6, '七' : 7, '八' : 8, '九' : 9, '零' : 0,
    '壹' : 1, '贰' : 2, '叁' : 3, '肆' : 4, '伍' : 5, '陆' : 6, '柒' : 7, '捌' : 8, '玖' : 9}
CN_UNIT = {
    '十' : 10,
    '拾' : 10,
    '百' : 100,
    '佰' : 100,
    '千' : 1000,
    '仟' : 1000,
    '万' : 10000,
    '萬' : 10000,
    '亿' : 100000000,
    '億' : 100000000,
    '兆' : 1000000000000,
}


def chinese_to_arabic(cn:str) -> int:
    unit = 0   # current
    ldig = []  # digest
    for cndig in reversed(cn):
        if cndig in CN_UNIT:
            unit = CN_UNIT.get(cndig)
            if unit == 10000 or unit == 100000000:
                ldig.append(unit)
                unit = 1
        else:
            dig = CN_NUM.get(cndig)
            if unit:
                dig *= unit
                unit = 0
            ldig.append(dig)
    if unit == 10:
        ldig.append(10)
    val, tmp = 0, 0
    for x in reversed(ldig):
        if x == 10000 or x == 100000000:
            val += tmp * x
            tmp = 0
        else:
            tmp += x
    val += tmp
    return val



def numberdetection(userstr):
   
#    patternnumber = re.compile('([一二三四五六七八九零十百千万亿]+|[0-9]+[]*[0-9])')
    patternnumber = re.compile('[一二三四五六七八九零十百千万亿0-9]*')
    lesspattern  = re.compile('不到|不足|差点|差点儿|欠点|差一点|差一点儿|欠一点|欠点儿|欠一点儿|没有')
    largerpattern1  = re.compile('超过|超了|上')
    largerpattern2  = re.compile('超|多|大')


    unitpattern1 = re.compile('元|块')#xx块豆腐难以处理
    unitpattern2 = re.compile('价格|价钱')
    disturbpattern1 = re.compile('瓶|杯|箱|米|步|碗|个|只|串|盘')
    disturbpattern2 = re.compile('面积|占地|空间|大小')
    
    
    allr_past = patternnumber.findall(userstr)

    allr = [lr for lr in allr_past if lr != '']
    numbers = []
    lesslarger = []
    isdistrub = []
    isarea = []
    prePos = 0
    print(allr)
    for i in allr:
        #print(i)
        if i == '一':
            continue
        #print('*')
        nPos=allr_past.index(i)
        #print(nPos)
        
        #根据数字前后信息判断是小于，大于，还是约等于
        r=0
        result = lesspattern.findall(userstr, nPos-4, nPos+6)
        if len(result):
            r=r-1
            #print(result)
        result = largerpattern1.findall(userstr, nPos-5, nPos+6)
        if len(result):
            r=r+1
            #print(result)
        result = largerpattern2.findall(userstr, nPos-1, nPos+len(i)+1)
        if len(result):
            r=r+1
            #print('here')
        lesslarger.append(r)
            
        #根据数字前后信息判断是否为干扰类
        r=0;
        result = disturbpattern1.findall(userstr, nPos, nPos+6)

        if len(result):
            r=1
        result = disturbpattern2.findall(userstr, nPos-4, nPos) 
        if len(result):
            r=1
        isdistrub.append(r)
        
        #根据数字前后信息判断是否为价格类
        r=0;
        result = unitpattern1.findall(userstr, nPos, nPos+6) 
        if len(result):
            r=1
        result = unitpattern2.findall(userstr, nPos-4, nPos) 
        if len(result):
            r=1
        isarea.append(r)        
            
        if i.isdigit():
            numbers.append(i)
        else:
            numbers.append(chinese_to_arabic(i))

        #print(i)
        #print(nPos)
        delete_record = []
        for i in isdistrub:
            if i == 1:
                index =isdistrub.index(i)
                del numbers[index]
                del lesslarger[index]
                del isarea[index]
                del isdistrub[index]

    print(numbers, lesslarger, isdistrub, isarea)
    return numbers, lesslarger, isdistrub, isarea



#for the question of area
def areajudgment2(userstr):
# print('啦啦啦')
    [numbers, lesslarger, isdisturb, isarea] = numberdetection(userstr)
    print([numbers, lesslarger, isdisturb, isarea])
    #relevantpattern  = re.compile('房间|卧室|工位|书房|床|客厅|教室|宿舍|办公|会议|茶水间|咖啡厅|饭厅|食堂')
    relevantpattern  = re.compile('售价|报价|零售|诚惠')
    
    if len(numbers) < 1:
        releventresult = relevantpattern.findall(userstr)
        if len(releventresult) > 0:
            return 4
        return 0    
    if sum(isdisturb) == len(isdisturb): #全部都是干扰信息
        return 0
    
    
    result = 0
    down = -1
    up = 100
    rightarea = -49
    #extract data

    
    for i in range(len(numbers)):
        if isdisturb[i] > 1:
            continue
        if lesslarger[i] == -1:  # less
                up =  float(numbers[i])
                print('up')
                print(up)
        if lesslarger[i] == 1: #larger
                down = float(numbers[i])
                print('down')
                print(down)
        if lesslarger[i] == 0: #larger
                print('rightarea:'+str(numbers[i]))
                rightarea = float(numbers[i])                
    
    if down > 40 or  rightarea > 40 or up <1:
        return 3    
    if rightarea >0 and rightarea <=20:
        return 1    
    if rightarea > 20 and rightarea <= 40:
        return 2
    
    if down <= 20 and up > 0:
        return 1
    
    if down > 20 and down < 40:
        return 2   
    
    return 4

#for other  questions
def areajudgment01(userstr):
    [numbers, lesslarger, isdisturb, isarea] = numberdetection(userstr)
 
    if len(numbers) < 1:
        return 0    
    if sum(isarea) == 0: #没有任何面积信息
        return 0
    
    down = -1
    up = 100
    rightarea = -49
    #extract data

    
    for i in range(len(numbers)):
        if isarea[i] == 0:
            continue
        if lesslarger[i] == -1:  # less
                up =  float(numbers[i])
                print('up')
                print(up)
        if lesslarger[i] == 1: #larger
                down = float(numbers[i])
                print('down')
                print(down)
        if lesslarger[i] == 0: #larger
                rightarea = float(numbers[i])                
    
    if down > 40 or  rightarea > 40 or up <1:
        return 3    
    if rightarea >0 and rightarea <=20:
        return 1    
    if rightarea > 20 and rightarea <= 40:
        return 2
    
    if down <= 20 and up > 0:
        return 1
    
    if down > 20 and down < 40:
        return 2   
    
    return 4


# qindex 2 面积问题 否则 其他
#返回
#0: 无关
#1： <=50
#2: 50< <=100
#3: >100
#4：矛盾 或者 确定不了，比如 大于50  小于 150
def areajudgment(userstr, qindex):
    result = 0
    if qindex == 2:
        result = areajudgment2(userstr)
    else:
        result = areajudgment01(userstr)
    return result

 
#0: 无关
#1： <=50
#2: 50< <=100
#3: outofrange
#4：矛盾 或者 确定不了，比如 大于50  小于 150

if __name__=='__main__':
    teststr = '2瓶水，我想要20以上的'
    print(teststr)
    #[numbers, lesslarger, isdisturb, isarea] = numberdetection(teststr)
    result = numberdetection(teststr)
    '''
    if(result == 0):
        print('对不起你跑题了')
    if(result == 1):
        print('好的，我们有实惠的推荐')
    if(result == 2):
        print('好啊，我们有相关的推荐')
    if(result == 3):
        print('对不起，不知道哪里有呢')
    if(result == 4):
        print('对不起，我蒙圈了')
    '''