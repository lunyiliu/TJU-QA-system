from answer_analysis import analysis
from judge_thinking import thinking
from 询问推荐 import recommand
from judge_fuzing import fuzzy
from judge_cross import cross
import pymysql
from random import choice
from reply_tuling import get_response
from reply_chat import comunication,messy,memory
import sys
sys.path.append(r'G:\project QA\前期版本\处理用户提问')
from 处理问题 import handle_question

record_times = [0,1,2]
conn = pymysql.connect(host='localhost', user='root', passwd='root', db='smart_qa', charset='utf8')
cursor = conn.cursor()

fenlei_list = ['自助餐','其他','甜点饮品','火锅烤肉','日韩料理','西餐','面食粥点','地方菜系','小吃快餐','家常菜','汉堡披萨']
didian_list = ['白堤路/风荷园','海光寺/六里台','王顶堤/华苑','体院北','南开/天大校区','西康路沿线','鞍山西道','鞍山道沿线','水上/天塔','天拖地区']


user_id = '123456'
answer = '123456'
groove0 = [[-3, -3, -3, -3, -3, -3, -3, -3, -3, -3,-3,-3] , [-3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3] ,  [[],[],[],[]], 1, 1, 1]

start = '您好，我可以向您推荐校内外的美食哦~<br/>首先咨询您几个问题'
pull = '哈哈，咱们回到刚刚的问题吧~'
prelpy = '我们的价格差不多'

ques = {1:'想去那里吃饭?',
        0:'想吃点什么呢?',
        2:'这顿饭的预算是多少?'}

sta_position = {1:'校内',
              2:'校外',
				}

sta_price =    {1:'20元以内',
              2:'20到30元',
              3:'30元以上',
              4:'都行'}

sta_type   = {
              1:'炒菜',
              2:'面',
              3:'盖饭',
              4:'都行'}
sample = [[-3, -3, -3, -3, -3, -3, -3, -3, -3, -3,-3,-3] , [-3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3] ,  [[],[],[],[]]]
def have_word_in_specify_list(word_list, str_temp):
    for word in word_list:
        if word in str_temp:
            return True
    return False


def robot_qa(user_id, answer, groove0,record_times):
    question_index = 0
    result_reply = []
    question_words = ['吗','呢','?','？','怎么','怎样','问','哪','有没有','是不是','什么']
    if have_word_in_specify_list(question_words,answer):
        question_index =1
        if '百年老店' in answer:
            result_reply = ['对不起我听不懂你再问什么内容呢~可以换种我听得懂的说法吗']
        else:
            print('try to answer')
            answers = []
            answers_ = []
            '''
            if '。' in answer:
                answers_ = answer.split('。')
                answers_ = list(filter(None, answers_))
                print(answers_)
            else:
                answers_.append(answer)
            for j in answers_:
                if '，'in j:
                    for k in j.split('，'):
                        answers.append(k)
                else:
                    answers.append(j)
            '''
            #answers = list(filter(None, answers))
            #print('split',answer.split('？'))
            #如果句子里有问号
            #print('answers:',answers)
            if '？' in answer:
                for i in range(len(answer.split('？'))):
                    if i != len(answer.split('？')) - 1:
                        u = answer.split('？')[i] + '？'
                        print('u', u)
                        if u != '':
                            answers.append(u)
            print('answers:',answers)
            '''
            if len(answer.split('？')) >=2:
                print('tes')
                for i in range(len(answers)):
                    print(answers[i])
                    if '？' in answers[i]:
                        print('tes2')
                        for j in range(len(answers[i].split('？'))):
                            if j != len(answers[i].split('？')) -1:
                                u = answers[i].split('？')[j] + '？'
                                print('u',u)
                                if u != '':
                                    answers.append(u)
                    answers.remove(answers[i])
            print('answers_split',answers)
            '''
            if str(answer) != str(user_id):
                result_reply = []
                print('answers',answers)

                for an in answers:
                    try:
                        print('try to answer3')
                        print('an',an)
                        result1 =  handle_question(an)
                        print(result1)
                        result_reply.append(result1)
                    except Exception as e:
                        print(e)
                        pass
                index = 0
                print('result_reply',result_reply)
                for i in result_reply:
                    if i == [] or i ==[[]] or i =='':
                        pass
                    else:
                        index = 1
                if index == 0:
                    result_reply.append('对不起我听不懂你再问什么内容呢~可以换种我听得懂的说法吗')
    print(result_reply)

    if groove0[-1] == 1:
        reply = ''

        if result_reply != [[]]:
            for i in result_reply:
                if i != [] and i != '':
                    reply += i
        if question_index == 0:
            is_own, own_reply = comunication(answer)
            if is_own == 0:
                isresponse, tuling = get_response(answer)
                if isresponse:

                    reply += tuling

                else:

                    reply += '我没能理解您在说什么。'

            else:
                reply = own_reply
        return  user_id, reply, groove0,record_times
    copy = [x for x in groove0]
    #    #二轮问答
    #    if groove0[5]==1:

    # 是否问答开始
    if str(answer) == str(user_id):
        ques_id = choice([0, 1, 2])
        answer = ques[ques_id]
        reply = ''

        if result_reply != [[]]:
            for i in result_reply:
                if i != [] and i != '':
                    reply += i
        reply += start + '<br/>' + answer


        groove0[4] = ques_id
        return user_id, reply, [[-3, -3, -3, -3, -3, -3, -3, -3, -3, -3,-3,-3] , [-3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3] ,  [[],[],[],[]], ques_id, 0, 0],record_times

        # 语义分析
    groove, status = analysis(answer, groove0,question_index)
    print('groove:', groove)

    if groove[3] in record_times:
        record_times.remove(groove[3])
    # 用户是否回答问题，
    if groove[groove[3]] != sample[copy[3]]:


        status = 2

    # step0:判断是否结束
    if groove[0] != [-3, -3, -3, -3, -3, -3, -3, -3, -3, -3,-3,-3] and groove[1] != [-3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3] and groove[2] !=  [[],[],[],[]] and record_times ==[] and groove[-1] == 0:
        reply = ''

        if result_reply != [[]]:
            for i in result_reply:
                if i != [] and i != '':
                    reply += i
        reply += user_recommand(groove)
        groove[-1] = 1
        return user_id, reply, groove,record_times
    print('-')

    # step1:判断是否乱码,再见
    possible = cross(answer)
    '''
    if possible == 0:
        reply = ''

        if result_reply != [[]]:
            for i in result_reply:
                if i != [] and i != '':
                    reply += i
        reply += messy() 

        groove[4] += 1
        return user_id, reply, groove,record_times
    '''
    if possible == 2:
        reply = ''

        if result_reply != [[]]:
            for i in result_reply:
                if i != [] and i != '':
                    reply += i
        reply += '很高兴为您服务，祝您吃得开心！'

        groove[4] += 1
        return user_id, reply, groove,record_times

    print('--')
    # step3:思考
    if thinking(answer):
        reply = ''

        if result_reply != [[]]:
            for i in result_reply:
                if i != [] and i != '':
                    reply += i
        reply += '好的，您再想想。'

        groove[4] += 1
        return user_id, reply, groove,record_times

    # step4:解析：正面回答
    print('---', status)
    #不会获取关键词直接推荐
    '''
    if  recommand(answer):
        groove_copy = groove
        if groove_copy[0] ==  [-3, -3, -3, -3, -3, -3, -3, -3, -3, -3,-3,-3]:
            groove_copy[0][-1] =1
        if groove_copy[1] ==[ -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3]:
            groove[1][-1] = 1
        if groove_copy[2] ==  [[], [], [],[]]:
            groove_copy[2] = [['100'],[0],[0],[0]]
        reply = ''

        reply = user_recommand(groove_copy)

        if result_reply != []:
            for i in result_reply:
                reply +=i

        groove[4] += 1
        return user_id,reply,groove,record_times
    '''
    if status == 2 :

        loc = []

        record_times = list(set(record_times))
        if groove[0] == [-3, -3, -3, -3, -3, -3, -3, -3, -3, -3,-3,-3]:
            loc.append(0)
        if groove[1] == [ -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3]:
            loc.append(1)
        if groove[2] == [[], [], [],[]]:
            loc.append(2)
        if loc == []:
            ques_id = choice(record_times)

        else:
            ques_id = choice(loc)
        print('loc',loc)
        print('record',record_times)
        reply = ''

        if result_reply != [[]]:
            for i in result_reply:
                if i != [] and i != '':
                    reply +=i
        reply += memory() + '<br/>' + ques[ques_id]


        groove[3] = ques_id
        groove[4] = 0
        return user_id, reply, groove,record_times

        # step52:解析：相关资讯
    if status == 1  or groove[groove[3]] == groove0[groove[3]] :
        reply = ''

        if result_reply != [[]]:
            for i in result_reply:
                if i != [] and i != '':
                    reply += i
        pull = '咱们回到刚刚的问题吧~'
        reply += '<br/>' + pull + ques[groove[3]]

        groove[4] += 1
        return user_id, reply, groove,record_times

        # step2:不想回答问题
    if fuzzy(answer)[0] == 1:
        reply = ''

        if result_reply != [[]]:
            for i in result_reply:
                if i != [] and i != '':
                    reply += i
        reply += fuzzy(answer)[1]

        groove[4] += 1
        return user_id, reply, groove,record_times

    # step5:解析：闲聊
    if status == 0 and (result_reply == [] or result_reply == [[]]):
        pull = '咱们回到刚刚的问题吧~'
        # 三句闲聊一拉回
        if groove[4] % 2 != 0:
            pull = ''
        else:
            pull = '<br/>' + pull + ques[groove[3]]

        is_own, own_reply = comunication(answer)
        if is_own == 0:
            isresponse, tuling = get_response(answer)
            if isresponse:
                reply = ''

                if result_reply != [[]]:
                    for i in result_reply:
                        if i != [] and i != '':
                            reply += i
                reply += tuling + pull

            else:
                reply = ''

                if result_reply != [[]]:
                    for i in result_reply:
                        if i != [] and i != '':
                            reply += i
                reply += '我没能理解您的答案。'

        else:
            reply = own_reply + pull
        groove[4] += 1
        return user_id, reply, groove,record_times

def user_recommand(groove):
    ending0 = "好的。"
    # office = "您想去哪：" + sta_office[groove[0]] + '<br/>'
    # fog = "您对除霾的需求：" + sta_fog[groove[1]] + '<br/>'
    # area = "您的使用面积：" + sta_area[groove[2]] + '<br/>'
    # product = get_product(groove) + '<br/>'
    caipin = []
    didian = []
    jiage = 0

    if groove[0][-1] == 1:
        for i in range(len(groove[0][:-1])):
            if groove[0][i] != -1:
                caipin.append(i)

    else:
        for i in range(len(groove[0][:-1])):
            if groove[0][i] == 1:
                caipin.append(i)

    if groove[1][-1] == 1:
        for i in range(len(groove[1][:-1])):
            if groove[1][i] != -1:
                didian.append(i)
    else:
        for i in range(len(groove[1][:-1])):
            if groove[1][i] == 1:
                didian.append(i)
    for i in range(len(caipin)):
        caipin[i] = fenlei_list[caipin[i]]
    for i in range(len(didian)):
        didian[i] = didian_list[didian[i]]

    if len(groove[2][0]) == 1 and groove[2][1][0] == 1:
        jiage = [int(groove[2][0][0]), 100]  # 大于0，小于数字
    if len(groove[2][0]) == 1 and groove[2][1][0] != 1:
        jiage = [0.8*int(groove[2][0][0]), 1.2*int(groove[2][0][0])]
    elif len(groove[2][0]) == 2:  # 20-30 或者20上下2元
        if int(groove[2][0][0]) >= int(groove[2][0][1]) and int(groove[2][0][1]) <= 10:
            jiage = [int(groove[2][0][0]) - int(groove[2][0][1]), int(groove[2][0][1]) + int(groove[2][0][0])]
        elif int(groove[2][0][0]) <= int(groove[2][0][1]) and int(groove[2][0][0]) <= 10:
            jiage = [-int(groove[2][0][0]) + int(groove[2][0][1]), int(groove[2][0][1]) + int(groove[2][0][0])]
        elif int(groove[2][0][0]) >= int(groove[2][0][1]) and int(groove[2][0][1]) > 10:
            jiage = [int(groove[2][0][1]), int(groove[2][0][0])]
        elif int(groove[2][0][0]) <= int(groove[2][0][1]) and int(groove[2][0][1]) > 10:
            jiage = [int(groove[2][0][0]), int(groove[2][0][1])]
        # 三个数字另作考虑
    print(caipin)
    print(didian)
    print(jiage)

    db = 'select * from meituan_overall where '
    if caipin != []:
        self = '('

        for i in caipin:
            self += '菜品种类=%s or '
        self = self[:-3]
        self = self + ')'
        db += self

        db += ' and '
    if didian != []:
        self = '('
        for i in didian:
            self += '地区=%s or '
        self = self[:-3]
        self = self + ')'
        db += self
    print(db)
    temp = []
    value = caipin + didian
    print(value)
    cursor.execute(db, value)
    conn.commit()
    temp = cursor.fetchall()
    print(temp)
    # 返回最多三个选择
    result = []
    for i in temp:

        if jiage[0] <= int(i[4]) < jiage[1]:
            name = i[0]
            cai = i[1]
            if int(i[4]) != 0:
                jia = i[4]
            else:
                jia = '--'
            pinfen = i[5]
            db_dian = 'select 详细地址 from meituan_detail where 商店名称= %s'
            cursor.execute(db_dian, i[0])
            conn.commit()
            di = cursor.fetchall()
            print(di)
            if di is None or di == '' or di == ():
                di_di = '--'
            else:
                di_di = di[0][0]
            self = [name, cai, jia, pinfen, di_di]
            result.append(self)
            if len(result) > 2:
                break
    print(result)
    if len(result) == 0 and len(temp) == 0:
        reply = '对不起，没有找到满足你价格需要的店。'

    elif len(result) == 0 and len(temp) != 0:
        reply = '对不起没有满足你价格需要的店，但是你可以试试这个。'

        if int(temp[0][4]) != 0:
            jia = temp[0][4]
        else:
            jia = '--'

        db_dian = 'select 详细地址 from meituan_detail where 商店名称= %s'
        cursor.execute(db_dian, i[0])
        conn.commit()
        di = cursor.fetchall()

        replt_ = '向您推荐' + str(temp[0][0]) + ',<br/>他主要经营' + str(temp[0][1]) + ',店内均价为 ' + str(
            jia) + '元，<br/>综合评分达到 ' + str(temp[0][5]) + '分。<br/>如果想去的话，它的详细地址是 ' + str(di[0][0])
        reply+=replt_
    elif len(result) == 1:
        reply = '向您推荐' + str(result[0][0]) + ',<br/>他主要经营' + str(result[0][1]) + ',<br/>店内均价为 ' + str(
            result[0][2]) + '元，<br/>综合评分达到 ' + str(result[0][3]) + '分。<br/>如果想去的话，它的详细地址是 ' + str(result[0][-1])

    else:
        reply = '向您推荐' + str(result[0][0]) + '和' + str(result[1][0]) + ',<br/>分别主要经营' + str(result[0][1]) + '和' + str(
            result[1][1]) + ',<br/>店内均价分别为为 ' + str(
            result[0][2]) + '和' + str(result[1][2]) + '元，<br/>综合评分达到 ' + str(result[0][3]) + '和' + str(
            result[1][3]) + '分。<br/>如果想去的话，它们的详细地址分别是 ' + str(result[0][-1]) + '和' + str(result[1][-1])


    #ending1 = " "
    reply = ending0 + reply #+ ending1
    return reply
