"""
Created on Sun Mar 24 10:58:29 2019

@author: Administrator
"""

from answer_analysis import analysis
from judge_thinking import thinking
from judge_price import price
from judge_fuzing import fuzzy
from judge_cross import cross
from random import choice
from reply_tuling import get_response
from reply_chat import comunication,messy,memory


user_id = 123456
answer = 123456
groove0 = [0, 0, 0, 1, 1,1]

start = '您好，我可以向您推荐校内外的美食哦~<br/>首先咨询您几个问题'
pull = '哈哈，咱们回到刚刚的问题吧~'
prelpy = '我们的价格差不多'

ques = {0:'想去校内还是校外吃饭?',
        1:'想吃面，炒菜，还是盖饭?',
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

result_position={1:'五食堂',
				 2:'四季村'}
result1=['三楼炒菜窗口，经济实惠','炒菜小店，经济实惠','二楼炒菜窗口，美味健康','家常菜馆，美味健康','三楼麻辣烫窗口，量多管饱','高档饭店，量多管饱']
result2=['三楼诺通拉面，经济实惠','牛肉面馆，经济实惠','二楼重庆小面，美味健康','韩国泡面，美味健康','三楼兰州拉面，量多管饱','兰州拉面，量多管饱']
result3=['三楼大碗饭，经济实惠','韩国石锅饭，经济实惠','二楼清真盖饭，美味健康','满堂红炒饭，美味健康','三楼鸡排饭，量多管饱','鸡公煲，量多管饱']
def get_product(groove):
    result="为您推荐："+result_position[groove[0]]
    if groove[1]=1 and groove[2]==1:
        if 	groove[0]==1:
            result+=result1[0]		
		else:
            result+=result1[1]           		
	if  groove[1]=1 and groove[2]==2:
        if 	groove[0]==1:
            result+=result1[2]		
		else:
            result+=result1[3]  
	if  groove[1]=1 and groove[2]==3:
        if 	groove[0]==1:
            result+=result1[4]		
		else:
            result+=result1[5]  
	if  groove[1]=1 and groove[2]==4:
        if 	groove[0]==1:
            result+=result1[choice([0,2,4])]		
		else:
            result+=result1[choice([1,3,5])]  
	if groove[1]=2 and groove[2]==1:
        if 	groove[0]==1:
            result+=result1[0]		
		else:
            result+=result1[1]       
	if  groove[1]=2 and groove[2]==2:
        if 	groove[0]==1:
            result+=result1[2]		
		else:
            result+=result1[3]  
	if  groove[1]=2 and groove[2]==3:
        if 	groove[0]==1:
            result+=result1[4]		
		else:
            result+=result1[5]  
	if  groove[1]=2 and groove[2]==4:
        if 	groove[0]==1:
            result+=result1[choice([0,2,4])]		
		else:
            result+=result1[choice([1,3,5])]  
	if  groove[1]=3 and groove[2]==1:
        if 	groove[0]==1:
            result+=result1[0]		
		else:
            result+=result1[1]    
	if  groove[1]=3 and groove[2]==2:
        if 	groove[0]==1:
            result+=result1[2]		
		else:
            result+=result1[3]  
	if  groove[1]=3 and groove[2]==3:
        if 	groove[0]==1:
            result+=result1[4]		
		else:
            result+=result1[5]  
	if  groove[1]=3 and groove[2]==4:
        if 	groove[0]==1:
            result+=result1[choice([0,2,4])]		
		else:
            result+=result1[choice([1,3,5])]  
	if  groove[1]=4 and groove[2]==1:
        if 	groove[0]==1:
            a=choice([1,2,3])	
            if a==1:
                result+=result1[0]
            if a==2:
                result+=result2[0] 	
            if a==3:
                result+=result3[0] 					
		else:
            a=choice([1,2,3])	
            if a==1:
                result+=result1[1]
            if a==2:
                result+=result2[1] 	
            if a==3:
                result+=result3[1] 	
	if  groove[1]=4 and groove[2]==2:
        if 	groove[0]==1:
            a=choice([1,2,3])	
            if a==1:
                result+=result1[2]
            if a==2:
                result+=result2[2] 	
            if a==3:
                result+=result3[2] 					
		else:
            a=choice([1,2,3])	
            if a==1:
                result+=result1[3]
            if a==2:
                result+=result2[3] 	
            if a==3:
                result+=result3[3] 	
	if groove[1]=4 and groove[2]==3:
        if 	groove[0]==1:
            a=choice([1,2,3])	
            if a==1:
                result+=result1[4]
            if a==2:
                result+=result2[4] 	
            if a==3:
                result+=result3[4] 					
		else:
            a=choice([1,2,3])	
            if a==1:
                result+=result1[5]
            if a==2:
                result+=result2[5] 	
            if a==3:
                result+=result3[5] 	
	if groove[1]=4 and groove[2]==4:
        if 	groove[0]==1:
            a=choice([1,2,3])	
            if a==1:
                result+=result1[choice([0,2,4])]
            if a==2:
                result+=result2[choice([0,2,4])] 	
            if a==3:
                result+=result3[choice([0,2,4])] 					
		else:
            a=choice([1,2,3])	
            if a==1:
                result+=result1[choice([1,3,5])]
            if a==2:
                result+=result2[choice([1,3,5])] 	
            if a==3:
                result+=result3[choice([1,3,5])] 
return result

def robot_airclean(user_id,answer,groove0):
    copy = [x for x in groove0]
#    #二轮问答
#    if groove0[5]==1:
        
    #是否问答开始
    if str(answer)==str(user_id):
        ques_id = choice([0,1,2])
        answer = ques[ques_id]
        reply = start+'<br/>'+answer
        groove0[4] = ques_id
        return user_id,reply,[0,0,0,ques_id,0,0]  
    
    #语义分析
    groove,status = analysis(answer,groove0)
    print('groove:',groove)
    
    #用户是否回答问题，
    if groove[groove[3]] != copy[copy[3]]:
        status = 2
    
    #step0:判断是否结束
    if groove[0]!=0 and groove[1]!=0 and groove[2]!=0:
        ending0 = "小智了解到："+'<br/>'
        office = "您的使用场合：" + sta_office[groove[0]] +'<br/>'
        fog = "您对除霾的需求：" + sta_fog[groove[1]] +'<br/>'
        area =  "您的使用面积：" + sta_area[groove[2]] +'<br/>'
        product = get_product(groove)+'<br/>'
        ending1 = "感谢您的使用，再见~"
        reply = ending0 + office + fog + area + product +ending1
        
        groove = [5,5,5,5,5,5]
        return user_id,reply,groove
    print('-')


    #step1:判断是否乱码,再见
    possible = cross(answer)
    if possible==0:
        reply = messy() 
        groove[4]+=1
        return user_id,reply,groove
    if possible==2:
        reply =  '很高兴为您服务，祝您生活愉快！'     
        groove[4]+=1
        return user_id,reply,groove

    print('--')
    #step3:思考 
    if thinking(answer):
        reply = '好的，您再想想。'   
        groove[4]+=1
        return user_id,reply,groove
    
    
    
    #step4:解析：正面回答 
    print('---',status)
    if status == 2 and groove[1]<4 and groove[2]<4:
        
            
        loc = [i for i,v in enumerate(groove[:3]) if v==0]
        assert len(loc)>0
        ques_id = choice(loc)
        if price(answer):
            reply = memory()+ '<br/>'+'价格详情，请查询www.jiashiqi.com'+'<br/>'+'下个问题：'+ ques[ques_id]
#        if price(answer) and groove[3]==1:
#            reply = memory()+ '<br/>'+'我们的除霾'
#        if price(answer)==0:
            
        else:
            reply = memory()+ '<br/>'+ ques[ques_id]
        groove[3] = ques_id
        groove[4] = 0
        return user_id,reply,groove
    
    #step51:解析：价格咨询    
    if price(answer):
        if groove[3]==0:
            reply = '办公室比家用的贵50，价格详情，请查询www.jiashiqi.com'+'<br/>'+'请问：'+ ques[groove[3]]
        if groove[3]==1:
            reply = '除霾功能的贵50，价格详情，请查询www.jiashiqi.com'   +'<br/>'+'请问：'+ ques[groove[3]]     
        if groove[3]==2:
            reply = '价格详情，请查询www.jiashiqi.com'+'<br/>'+'请问：'+ ques[groove[3]]
        groove[4]+=1
        return user_id,reply,groove    
        
    #step52:解析：相关资讯      
    if status == 1 or groove[1]==4 or groove[2]==4 :
        pull = '咱们回到刚刚的问题吧~'
        reply = '详情请参见我们的网页www.jiashiqi.com.'+ '<br/>' +pull+ ques[groove[3]]
        groove[4]+=1
        return user_id,reply,groove    

    #step2:不想回答问题
    if fuzzy(answer)[0]==1:
        reply = fuzzy(answer)[1]
        groove[4]+=1
        return user_id,reply,groove
    
    
    #step5:解析：闲聊  
    if status == 0:
        pull = '咱们回到刚刚的问题吧~'
        #三句闲聊一拉回
        if groove[4]%2!=0:  
            pull = ''
        else:
            pull = '<br/>' + pull + ques[groove[3]]
            
        is_own,own_reply = comunication(answer)  
        if is_own==0:
            isresponse,tuling = get_response(answer)
            if isresponse:
                reply = tuling + pull
            else:
                reply = '宝宝没有理解您的答案。'
        else:
            reply = own_reply + pull
        groove[4]+=1
        return user_id,reply,groove
