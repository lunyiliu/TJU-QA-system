from robot import robot_airclean

user_id = 123456
answer = 123456
groove = [0,0,0,0,0,0]
i = 0



while i < 10000000:
    print('#########################################')
    print('>>>', end=':')
    if i==0:
        answer = 123456
    else:
        answer = input()
    print(answer)
    user_id,reply,groove = robot_airclean(user_id,answer,groove)
    print('$&$&$&$&$&$&$&$&$&$&$&$&$&$&$&$&$&$&$&$&$')
    print('user_id:',user_id)
    print('reply:',reply)
    print('groove:',groove)
    print('$&$&$&$&$&$&$&$&$&$&$&$&$&$&$&$&$&$&$&$&$')
    i +=1
    if groove == [5,5,5,5,5,5]:
        break
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
    
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              
              

#        print(questionIDString)
#        print('>>>', end=':')
#        answer = input()
#        if len(answer) == 0:
#            while 1:
#                print('输入不能为空：')
#                answer = input()
#                if len(answer) > 0:
#                    break
#
#    else:
#        if i == 0:
#            i = 1
#            print('#########################################')
#            print('食材有什么？')
#            print('>>>', end=':')
#            questionLists = [i for i in range(2, 9)]
#            menuLists = [i for i in range(1, 50)]
#            questionID = 1
#            repeatNum = 0
#            answerID = 0
#            answer = input()
#            if len(answer) == 0:
#                while 1:
#                    print('输入不能为空：')
#                    answer = input()
#                    if len(answer) > 0:
#                        break
#
#        else:
#            print('#########################################')
#            print('>>>', end=':')
#            answer = input()
#            if len(answer) == 0:
#                while 1:
#                    print('输入不能为空：')
#                    answer = input()
#                    if len(answer) > 0:
#                        break
#    #
#
#    print('前questionID', questionID)
#    print('前Groove', Groove)
#
#    userID, sessionID, answerID, answerTag, emotionScore, menuLists, middle, unknowFlag, \
#    isPass, flag, repeatNum, question, questionID, questionLists, Groove = \
#        oc_tju_robot(userID, sessionID, answerID, answer, flag, repeatNum, middle, \
#                     questionID, questionLists, Groove)
#
#    if middle != '':
#        mid = [int(x) for x in middle.split(',')]
#        nameList = [getMenuName(x) for x in mid]
#        print('nameList', nameList)
#    print('后questionID', questionID)
#    print('menuLists', menuLists)
#    print('后Groove', Groove)
#
#    print('#######################################')
#    print('question', question)
#
#    questionIDString = getCataQuestion(questionID)
#    questionID = getIDQuestion(questionID)
#
#    if isPass == 3:
#        print('推荐完成')
#        print(menuLists)
#        break
#    i += 1
