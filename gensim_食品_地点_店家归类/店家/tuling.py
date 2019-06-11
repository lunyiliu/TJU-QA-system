#coding=utf8
import requests

KEY = '70e2d9bd106043aea6d02cf758eb4583'



def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        if r.get('code')==100000:
            return 1,r.get('text')
        else:
            return 0,0
    except:
        return 0,0
    
