import re


u0 = re.compile(u'[^a-zA-Z]')
u1 = re.compile(u'[^0-9]') # 否定词
ut2 = re.compile(u'(yes|bye|no|easy|good|well)') 
u3 = re.compile(u'[^\u4E00-\u9FA5]')
u4 = re.compile(u'(bye|再见|拜拜)')
def cross(answer):
    answers = answer.lower()
    hanzi = u3.sub(r'',answers)
    if len(hanzi) > 15:
        return 0
    if re.search(u4, answer)  and len(hanzi) < 5: 
        return 2
    alp = u0.sub(r'',answers)
    if re.search(ut2,alp):
        return 1
    if len(alp) == len(answers):
        return 0  # 可能是拼音
    if len(alp) > 5:
        return 0
#    num = u1.sub(r'',answers)
#    if len(num) == len(answers):
#        if len(num) < 3:
#            return 1
#        else:
#            return 0
#    if len(num) > 5:
#        return 0
#    if len(num) + len(alp) > 5:
#        return 0
    return 1
# question = '客官酸甜、麻辣您更喜欢哪一种？'
# while 1:
#     print(question)
#     answer = input()
#     polarity = judge_cross(answer)
#     print(polarity)