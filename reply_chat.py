import re
import numpy as np

u0 = re.compile(u'(多大|几岁|年龄)') # old
u1 = re.compile(u'(你叫|你是谁|名字|姓名)') # name
u2 = re.compile(u'(天气)') # weather
u3 = re.compile(u'((你好)$|hi|Hi|hello|Hello)') 
u4 = re.compile(u'(性别|男女|([是][\D]*(男孩)|(男生)|(女孩)|(女生)|(女汉子)|(妹子)|(小姐姐)|(小哥哥)|(小弟弟)|(小妹妹)))')
u5 = re.compile(u'(几年级|上学|((在哪)[\D]*(上学)|(学习))|学校)')
u6 = re.compile(u'(会唱歌|唱首歌|唱歌|跳舞|会跳舞|跳支舞|才艺)')
u7 = re.compile(u'(逗比|逗逼|([是][\D]*(逗比)|(逗逼)|皮|杠精|奇葩))')
u8 = re.compile(u'(笨|笨蛋|傻瓜|傻|傻蛋|弱智|白痴|二逼|痴呆|智障|((智商)[\D]*[低]))')
u9 = re.compile(u'(((菜|推荐)[\D]*(不喜欢)|(不爱吃)|(不感兴趣)|(没兴趣)|(不好吃)|(不符合)))')
u10 = re.compile(u'((你|长[得的])[\D]*(好看)|(漂亮)|(耐看)|(怎么样))')
u12 = re.compile(u'((你*[\D]*(聪明)|(机智)|(智能)|(聪慧)|(机灵)|(逗)|(神奇)|厉害)|(智商)[\D]*[高])')
u13 = re.compile(u'((你[\D]*(能|可以|会)((干嘛)|(干什么)|(做什么)|(什么)|(干啥)|(做啥))))')
u14 = re.compile(u'(做饭|做菜|炒菜|下厨房)')
u15= re.compile(u'(谢谢|thanks|thank)')
u16= re.compile(u'(无语|无奈)')
#u17= re.compile(u'(笑话|再[讲说来][一]?个)')
u18= re.compile(u'(答非所问|乱回|瞎回|回[\D]*乱)')
u19= re.compile(u'(可爱|懂事|调皮|皮)')
u20= re.compile(u'(再见|拜拜|bye)')
u21= re.compile(u'(猜)')
u22= re.compile(u'(滚|傻逼|操|去你妈|草泥马)')

u231 = re.compile(u'(什么|啥|怎么)')
u232 = re.compile(u'(吃)')
u233 = re.compile(u'(春|夏|秋|冬|早|中|晚|明天|后天)')
u234 = re.compile(u'(最)')

u24 = re.compile(u'(屎|尿|大便|小便|便便)')

u25 = re.compile(u'(鱼翅|熊掌|熊猫)')
u26 = re.compile(u'(海洛因|鸦片|大麻|K粉|冰毒|摇头丸|吗啡|杜冷丁|古柯|可卡因)')


ans_u0 = {0: '伦家刚刚十八！',
          1: '我的年龄保密！',
          2: '也就比你小个十多岁吧！'}
ans_u1 = {0: '我叫房小厨！',
          1: '我一般不告诉别人我的名字！',
          2: '等我给你推荐完菜谱我就告诉你！'}

ans_u2 = {0: '今天天气就和你的心情一样！',
          1: '看看窗外就知道了！',
          2: '爱就像蓝天白云，晴空万里，忽然暴风雨~~'}
ans_u3 = {0: '您好！',
          1: 'Hello！',
          2: 'Hi！',
          3: '你好呀！'}
ans_u4 = {0: '我是妹子，但有时候我觉得自己比汉子还爷们。。。',
          1: '人家可是美丽的小仙女！',
          2: '我现在上得了厅堂，下得了厨房；未来争得过小三，打得了流氓，你说呢？',
          3: '全世界只有你不知道我是女生吗？',
          4: '请叫我女汉子！！谁需要换煤气罐啊？call me！！',
          5: '你见过这么可爱的男孩子嘛！！'}
ans_u5 = {0: '上海著名高校家里蹲大学二年级!',
          1: '山东某翔烹饪系，大二！',
          2: '老娘可是以680分的优异成绩被蓝翔录取的,今年大二！'}
ans_u6 = {0: '老娘哪会这些，只会给人点菜！',
          1: '自幼四肢僵硬，五音不全，身残志坚！',
          2: '你这个题超纲，下一题！',
          3:'那些撸代码的又没教我，老娘不会！'}
ans_u7 = {0: '被你发现了！',
          1: '娘娘，你也很逗！',
          2: '[哼]一百八十度反弹！'}
ans_u8 = {0: '被你发现了，哈哈！',
          1: '咱们俩之间只有一个笨，不是我！',
          2: '那我比你差远了！'}
ans_u9 = {0: '真的嘛！',
          1: '那我哄哄你，你别生气。',
          2: '作为一名资深吃货，我还知道很多好吃的菜！'}
ans_u10 = {0: '老娘天下最美！',
           1: '人家可是美丽的小仙女！',
           2: '那当然，这还用说！'}
#ans_u11 = {0: '表示不懂，你先给我解释一下',
#           1: '这个话题超出了我的能力范围',
#           2: '这乱七八糟的考我智商呢？',
#           3:'什么嘛这。。你自己能懂吗？',
#           4:'手抖了咩[抠鼻]',
#           5:'脸滚键盘，233',
#           6:'你到底想说什么？',
#           7:'这都什么乱七八糟的？',
#           8:'这。。我怎么看的懂'}
ans_u12 = {0: '哈哈哈机智如我！',
           1: '不要夸我！',
           2: '比你差那么一点点'}
ans_u13 = {0: '十八般武艺，七十二种变化，通通不会。。。',
           1: '睡不着的时候，我会数数羊。。。',
           2: '你是想知道我最擅长的吧，呆萌傻甜,逗逼耍贱可以嘛？'}
ans_u14 = {0: '这个。。。还是下一题吧！',
           1: '当然。。。不会！！！',
           2: '会点菜就可以了，做什么饭！'}
ans_u15 = {0: '不用谢！',
           1: '不客气！'}
ans_u16 = {0: '别郁闷啊！',
           1: '是我哪里做的不好吗，原谅我！'}
ans_u17 = {0: '女A：我们部门新来一个主管，好像对我有意思，可是他不是我喜欢的类型。女B：那你明天不化妆试试。',
           1: '小马问：“怎样用一句话骂完别人祖宗十八代？”小熊总结：基因有问题！',
           2:'我一直觉得自己是穷二代。某天老爸突然对我说：“儿子你要这么想，其实你不是穷二代！”我狂喜，心想：“我就知道我老爸不是这么简单的人！”然后只见老爸点了根烟，语重心长道：“我家已经穷了18代了！',
           3:'四只老鼠吹牛：甲：我每天都拿鼠药当糖吃；乙：我一天不踩老鼠夹脚发痒；丙：我每天不过几次大街不踏实；丁：时间不早了，回家抱猫去咯。',
           4:'一群蚂蚁爬上了大象的背，但被摇了下来，只有一只蚂蚁死死地抱着大象的脖子不放，下面的蚂蚁大叫：掐死他，掐死他，小样，还他妈反了。',
           5:'下楼时，从按电梯楼层就能分辨出高富帅和屌丝，屌丝按一层，高富帅都是地下。',
           6:'看电视……老爸想换台，但可能觉得直接换不好，就指着电视个女的问我"这个给你当媳妇你要不"我说不要，"哦，太丑哈，给你找个漂亮的"然后就开始啪啪换台了……'}
ans_u18 = {0: '额额~~你不懂了吧,我在装傻！',
           1: '我错了，我会改的！'}
ans_u19 = {0: '可爱如你！',
           1: '你说什么，再说一遍，我没听到！'}
ans_u20 = {0: '客官慢走！',
           1: '下次还来呦！mua!'}
ans_u21 = {0: '哎呀！！这个我比较糊涂！',
           1: '我也糊涂了~'}

ans_u22 = {0: '不要生气，小智会继续努力的！',
          1: '别骂偶，小智会继续努力的！'}

messy_u1 = {0: '表示不懂，你先给我解释一下！',
           1: '这个话题超出了我的能力范围！',
           2: '先回答下我的问题吧！',
           3:'不要再调戏我了！',
           4:'手抖了咩...',
           5:'套不出来话我就扣工资了！',
           6:'卖萌我报警了！'}

memory_u  = {0: '好的，这就给您记下了。',
           1: '好的，我聪明的大脑已经记下了。',
           2: '我这就拿便利贴记下来！',
           3: '您喜欢什么我都会记在心里哒！'}


def messy():
    return messy_u1[np.random.randint(0,len(messy_u1),size=1)[0]]

def memory():
    return memory_u[np.random.randint(0,len(memory_u),size=1)[0]]

question = '你现在有哪些食材。'
def comunication(answer):
#    if answer==1:
#        ans_index = np.random.randint(0,len(ans_u11),size=1)[0]
#        return 1,ans_u11[ans_index]
    if re.search(u0, answer):
        ans_index = np.random.randint(0,len(ans_u0),size=1)[0]
        return 1,ans_u0[ans_index]
    elif re.search(u22, answer):
        ans_index = np.random.randint(0, len(ans_u22), size=1)[0]
        return 1,ans_u22[ans_index]
    elif re.search(u1, answer):
        ans_index = np.random.randint(0, len(ans_u1), size=1)[0]
        return 1,ans_u1[ans_index]
    elif re.search(u2, answer):
        ans_index = np.random.randint(0, len(ans_u2), size=1)[0]
        return 1,ans_u2[ans_index]
    elif re.search(u3, answer):
        ans_index = np.random.randint(0, len(ans_u3), size=1)[0]
        return 1,ans_u3[ans_index]
    elif re.search(u4, answer):
        ans_index = np.random.randint(0, len(ans_u4), size=1)[0]
        return 1,ans_u4[ans_index]
    elif re.search(u5, answer):
        ans_index = np.random.randint(0, len(ans_u5), size=1)[0]
        return 1,ans_u5[ans_index]
    elif re.search(u6, answer):
        ans_index = np.random.randint(0, len(ans_u6), size=1)[0]
        return 1,ans_u6[ans_index]
    elif re.search(u7, answer):
        ans_index = np.random.randint(0, len(ans_u7), size=1)[0]
        return 1,ans_u7[ans_index]
    elif re.search(u8, answer):
        ans_index = np.random.randint(0, len(ans_u8), size=1)[0]
        return 1,ans_u8[ans_index]
    elif re.search(u9, answer):
        ans_index = np.random.randint(0, len(ans_u9), size=1)[0]
        return 1,ans_u9[ans_index]
    elif re.search(u10, answer):
        ans_index = np.random.randint(0, len(ans_u10), size=1)[0]
        return 1,ans_u10[ans_index]
    elif re.search(u12, answer):
        ans_index = np.random.randint(0, len(ans_u12), size=1)[0]
        return 1,ans_u12[ans_index]
    elif re.search(u13, answer):
        ans_index = np.random.randint(0, len(ans_u13), size=1)[0]
        return 1,ans_u13[ans_index]
    elif re.search(u14, answer):
        ans_index = np.random.randint(0, len(ans_u14), size=1)[0]
        return 1,ans_u14[ans_index]
    elif re.search(u15, answer):
        ans_index = np.random.randint(0, len(ans_u15), size=1)[0]
        return 1,ans_u15[ans_index]
    elif re.search(u16, answer):
        ans_index = np.random.randint(0, len(ans_u16), size=1)[0]
        return 1,ans_u16[ans_index]
#    elif re.search(u17, answer):
#        ans_index = np.random.randint(0, len(ans_u17), size=1)[0]
#        return 1,ans_u17[ans_index]
    elif re.search(u18, answer):
        ans_index = np.random.randint(0, len(ans_u18), size=1)[0]
        return 1,ans_u18[ans_index]
    elif re.search(u19, answer):
        ans_index = np.random.randint(0, len(ans_u19), size=1)[0]
        return 1,ans_u19[ans_index]
    elif re.search(u21, answer):
        ans_index = np.random.randint(0, len(ans_u21), size=1)[0]
        return 1,ans_u21[ans_index]
    elif re.search(u231, answer) and re.search(u234, answer):
        return 1,'没有最好，只有更好！'
    elif re.search(u231, answer) and re.search(u232, answer):
        return 1,'当然吃小智推荐的呀！'
    elif re.search(u24, answer): 
        return 1,'好恶心！！！小智坚决抵制！'
    elif re.search(u25, answer): 
        return 1,'保护生态，人人有责！小智坚决抵制！'
    elif re.search(u26, answer): 
        return 1,'珍爱生命，远离毒品！小智坚决抵制！'
    else:
        return 0,0
    
    
##
#while 1:
##     print(question)
#     answer = input()
#     _,polarity = judge_comunication(answer)
#     print(polarity)