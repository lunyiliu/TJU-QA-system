import re
import numpy as np
from exmotion import sentiment

st0 = re.compile(u'(没问题|不错|没事|没有问题|没错)')  # 有否定词但是是肯定
st1 = re.compile(u'(不|算了)') # 否定词
st2 = re.compile(u'((很|挺|非常|太)*(好|棒|强|牛|厉害|聪明|满意|嗯|适合|流弊|优|赞|帅|屌)|(还|勉强)*(行|可以|尚可|阔以|ok|yes|good|凑合|凑和)|当然|必须|肯定)')
st3 = re.compile(u'(一般|垃圾|白痴|扯蛋|煞笔|辣鸡|废物|差|傻|中等|中评|勉勉强强|low|烂|忘记)')
st5 = re.compile(u'(想想|想一想|想一下|想下|说说)')
st6 = re.compile(u'(不过|要不|不能)')
que = re.compile(u'(好不好|要不要|有没有|行不行|能不能|可不可以|会不会|吗|什么|啥|哪)')


reply_pos  = {0: '哇塞，超开心的，感谢客官的肯定~~',
              1: '可把宝宝我牛X坏了，让我叉会腰！'}

reply_neg  = {0: '心塞塞，宝宝继续发育去了，记得过两天再来翻宝宝的牌子哟！',
              1: '忧桑，不过宝宝不会气馁的，记得过两天再来翻宝宝的牌子哟！'}

reply_none  = {0: '宝宝没有理解，但是宝宝会继续努力的，怀挺~~',
               1: '宝宝没有理解，偶要回家继续修炼去了，怀挺~~'}

reply_bye  = {0: '很高兴为您服务，祝您生活愉快！',
               1: '下次见，祝您生活愉快！'}

def posReply():
    return reply_pos[np.random.randint(0,len(reply_pos),size=1)[0]]

def negReply():
    return reply_neg[np.random.randint(0,len(reply_neg),size=1)[0]]

def noneReply():
    return reply_none[np.random.randint(0,len(reply_none),size=1)[0]]
def byeReply():
    return reply_bye[np.random.randint(0,len(reply_bye),size=1)[0]]


def judge_satisfied(answers):
    answer = answers.lower()
    if '再见' in answer or 'bye' in answer:
        return 1,byeReply()
    if re.search(que, answer) or re.search(st5, answer):
        return 0,noneReply()
    elif re.search(st0, answer):
        return 1,posReply()
    elif re.search(st1, answer) and not re.search(st6, answer):
        if re.search(st2, answer):
            return 2,negReply()
        elif re.search(st3, answer):
            return 1,posReply()
        else:
            return 2,negReply()
    elif re.search(st2, answer):
        return 1,posReply()
    elif re.search(st3, answer):
        return 2,negReply()
    else:
        score = sentiment.predict(answer)
        print(score)
        if score <= 0.33:
            return 2, negReply()
        if score >= 0.60:
            return 1, posReply()
        else:
            return 0,noneReply()

#q1 = '客官还满意我的推荐菜吗？'
#while 1:
#    question = q1
#    print(question)
#    answer = input()
#    _,polarity = judge_satisfied(answer)
#    print(polarity)