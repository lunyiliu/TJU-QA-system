import re
u0 = re.compile(u'(想想|想下|想一下|考虑|想一想|等一等|瞄一眼)')
u1 = re.compile(u'(等等)')
#u2 = re.compile(u'(不|没|算了|别|拒绝)') # 否定词
#u1 = re.compile(u'(不怕|不惧|不担心)') # 否定肯定词
#ut1 = re.compile(u'(简单|菜鸟|小白|新手|容易|好做|省事|挑战小|挑战低|上手|快|easy)') # “简单”
#ut2 = re.compile(u'(一般|中等|中间)') #  “一般”
#ut3 = re.compile(u'(难|复杂|挑战高|有挑战|挑战大)') #  “困难”
#u3 = re.compile(u'(都可以|都行|不挑|都想|随便|无所谓|都还行|随意)') # 通用

question = '我的菜谱有简单、一般和困难，今天想先试哪一种？'
def thinking(answer):
    if re.search(u0, answer):
        return 1
    if re.search(u1, answer):
        if len(answer) < 5:
            return 1
    return 0
