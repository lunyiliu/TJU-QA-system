# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 10:45:38 2019

@author: lenovvo
"""
import emoji
import time
from lxml import etree
from DB_handler import DB_handler
import requests
import json 
headers={
'Accept': 'application/json',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cookie': '__mta=120831415.1555468357017.1555487716115.1556088774617.13; rvct=30; iuuid=E0E56FF846843C10D248BDF57BC95AF9220866F38199FD9DB72FF6ACC6FAA4F0; _lxsdk_cuid=16a0d349feac8-0f892d3fc84788-58422116-144000-16a0d349febc8; _lxsdk=E0E56FF846843C10D248BDF57BC95AF9220866F38199FD9DB72FF6ACC6FAA4F0; webp=1; cityname=%E5%A4%A9%E6%B4%A5; wm_order_channel=mtib; _hc.v=05d786a3-de7e-21fd-8fb6-e4fac152bedc.1555468357; __utma=74597006.1402815768.1554999719.1555473417.1555476883.4; __utmz=74597006.1555476883.4.4.utmcsr=blog.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/xing851483876/article/details/81842329; ci=40; IJSESSIONID=mkl5rj5whncw17vbbkte8n9ot; _lx_utm=utm_source%3Dblog.csdn.net%26utm_medium%3Dreferral%26utm_content%3D%252Fxing851483876%252Farticle%252Fdetails%252F81842329; latlng=39.11417,117.153547,1556088723582; ci3=1; i_extend=C_b1Gimthomepagecategory11H__a; client-id=cbf09485-6355-4103-91a2-44212bae06fa; uuid=c7bac8c4-f183-463a-a35c-b29b3e003aec; logan_custom_report=; _lxsdk_s=16a4e1d9632-aaa-e11-16b%7C%7C26; logan_session_token=m1ni8uty1cghr4cnfe1q',
'Host': 'meishi.meituan.com',
'Referer':'',
'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36',
        }
def get_address_phone(poiid,ct_poi,header):
    url='https://meishi.meituan.com/i/poi/'+poiid+'?ct_poi='+ct_poi
    #print(url)
    while 1:
        try:
            text=requests.get(url,headers=header,timeout=5).text
            break
        except Exception as e:
            print(e)
    selector=etree.HTML(text)
    address_=selector.xpath("//div[@class='poi-address']")
    address=address_[0].xpath('string(.)').strip()
    #phone_=selector.xpath("//a[@class='btn msg-btn']")
    #phone=phone_[0].xpath('string(.)').strip()            
    return address
def get_comment(poiid):
    page_num=0
    content=''
    last='啦啦啦'
    last_two='啦啦啦'
    while 1:
        page_num+=1
        print('评论页数'+str(page_num))
        comment_url='https://i.meituan.com/poi/'+poiid+'/feedbacks/page_'+str(page_num)
        while 1:
            try:
                text=requests.get(comment_url,timeout=5).text
                break
            except Exception as e:
                print(e)
        selector=etree.HTML(text)
        if selector is not None:
            content_=selector.xpath("//div[@class='comment']")
        else:
            content_=[]
        if content_==[]:
            return emoji.demojize(content)
        for c in content_:
            con=c.xpath('string(.)').strip()
            if last=='啦啦啦':
                last=con
            else:
                last_two=last
                last=con     
            content+=con+';' 
            #print('last:'+last+',last_two:'+last_two)
            if (last=='' and last_two=='') or len(content)>1200:
                content=content.strip(';')
                return emoji.demojize(content)
'''
                effective_pattern = re.compile(
    u"([\u4e00-\u9fa5])|"  # emoticons
    u"([0-9])|"  # symbols & pictographs (1 of 2)
    u"([a-zA-Z])|"  # symbols & pictographs (2 of 2)
    u"(!?！？~，。;,；：“”、=-+)|"  # transport & map symbols
                )
                content_filtered=''
                for char in content:
                    if re.match(effective_pattern,char):
                        content_filtered+=char
'''
                


                
def get_dish(headers,payload):
    while 1:
        try:
            response=requests.post('https://meishi.meituan.com/i/api/dish/poi',headers=headers,data=payload,timeout=5)
            #print(payload)
            break
        except Exception as e :
            print(e)
            return ' '
    data=json.loads(response.text)
    if 'data' in data:
        dishes=data['data']['list']
        if dishes!=[]:
            dish_str=''
            for dish in dishes:
                dish_str+=dish['name']
                dish_str+=',%d元,'%(dish['price']/100)
            dish_str=dish_str.strip(',')
            return dish_str
        else:
            return ' '
    else:
        return ' '
     



payload={
'app': "",
'optimusCode': 10,
'partner': 126,
'platform': 3,
'poiId': 0,
'riskLevel': 1,
'originUrl':'',
'uuid': "c7bac8c4-f183-463a-a35c-b29b3e003aec",
'version': "8.3.3",
        }
DBh=DB_handler()
store_info=DBh.select(['meituan_overall'],['店名','ctPoi','Poiid'],[])
store=store_info[0]
ctpoi=store_info[1]
poiid=store_info[2]
for i in range(443,len(store)):
    print('第%d家店：%s'%(i,store[i]))
    originUrl="http://meishi.meituan.com/i/poi/"+poiid[i]+"?ct_poi="+ctpoi[i]
    payload['originUrl']=originUrl
    headers['Referer']=originUrl
    payload['poiId']=poiid[i]
    print(i)
    dish=get_dish(headers,payload)
    comment=get_comment(poiid[i])
    address=get_address_phone(poiid[i],ctpoi[i],headers)
    value=[store[i],address,dish,comment]
    DBh.insert('meituan_detail',value)
    time.sleep(2)
    
    