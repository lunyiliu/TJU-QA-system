# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 10:45:38 2019

@author: lenovvo
"""
from DB_handler import DB_handler
import requests
import json 
headers={
'Accept': 'application/json',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cookie': 'rvct=30; iuuid=E0E56FF846843C10D248BDF57BC95AF9220866F38199FD9DB72FF6ACC6FAA4F0; _lxsdk_cuid=16a0d349feac8-0f892d3fc84788-58422116-144000-16a0d349febc8; _lxsdk=E0E56FF846843C10D248BDF57BC95AF9220866F38199FD9DB72FF6ACC6FAA4F0; webp=1; ci=40; cityname=%E5%A4%A9%E6%B4%A5; IJSESSIONID=1jc03d5rxan3swjggtjyms64i; ci3=1; __utma=74597006.1402815768.1554999719.1554999719.1555467382.2; __utmc=74597006; __utmz=74597006.1555467382.2.2.utmcsr=blog.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/xing851483876/article/details/81842329; wm_order_channel=mtib; au_trace_key_net=default; _lx_utm=utm_source%3D60030; openh5_uuid=E0E56FF846843C10D248BDF57BC95AF9220866F38199FD9DB72FF6ACC6FAA4F0; uuid=E0E56FF846843C10D248BDF57BC95AF9220866F38199FD9DB72FF6ACC6FAA4F0; latlng=39.109386,117.162183,1555468345117; __utmb=74597006.4.9.1555468355614; i_extend=C_b1Gimthomepagecategory11H__a; _lxsdk_s=16a2914ab72-32f-1b3-654%7C%7C9; client-id=408bcb95-8d4d-41f3-ba92-6b71c5a5c591',
'Host': 'meishi.meituan.com',
'Referer': 'https://meishi.meituan.com/i/?ci=40&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1',
'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36',
        }
payload={
'app': "",
'areaId': 0,
'cateId': 1,
'deal_attr_23': "",
'deal_attr_24': "",
'deal_attr_25': "",
'limit': 20,
'lineId': 0,
'offset': 0,
'optimusCode': 10,
'originUrl': "http://meishi.meituan.com/i/?ci=40&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1",
'partner': 126,
'platform': 3,
'poi_attr_20033': "",
'poi_attr_20043': "",
'riskLevel': 1,
'sort': "distance",
'stationId': 0,
'uuid': "E0E56FF846843C10D248BDF57BC95AF9220866F38199FD9DB72FF6ACC6FAA4F0",
'version': "8.3.3",
        }
#p = {'https': '163.125.157.49:8888'}
DBh=DB_handler()
page=0
while page<10:
    print(page)
    payload['offset']=page*20
    while 1:
        try:
            response=requests.post('https://meishi.meituan.com/i/api/channel/deal/list',headers=headers,data=payload,timeout=5)
            break
        except Exception as e :
            print(e)
    data=json.loads(response.text)
    if 'data' in data and 'poiList' in data['data'] and 'poiInfos' in data['data']['poiList'] and len(data['data']['poiList']['poiInfos']):
        store_list=data['data']['poiList']['poiInfos']
        for store in store_list:
            value=[]
            value.append(store['name'])
            value.append(store['cateName'])
            value.append(store['areaName'])
            value.append(store['distance'])
            value.append(store['avgPrice'])
            value.append(store['avgScore'])
            value.append(store['ctPoi'])
            value.append(store['poiid'])
            smartTags=store['smartTags']
            if smartTags!=[]:
                tag=''
                for i,tag in enumerate(smartTags):
                    if i ==0:
                        tag=tag['text']['content']
                    else:
                        tag=tag+','+tag['text']['content']
            else:
                tag='Null'
            value.append(tag)
            print(value)
            DBh.insert('meituan_overall',value)
    page+=1
        
    
    