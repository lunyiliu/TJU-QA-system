import sys
from bottle import get,post,run,request,template,TEMPLATE_PATH,route,static_file
import os
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__
sys.path.append(r'C:\Users\lenovvo\Desktop\吴偶教授\天津大学智能问答\天大美食智能问答\前期版本')
from robot import robot_airclean
from robot import get_product

global groove,user_id
groove = [0, 0, 0, 1, 1, 0]
user_id = 123456
#print(1)

TEMPLATE_PATH.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "view")))
assets_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets"))
@route('/assets/<filename:re:.*\.css|.*\.js|.*\.png|.*\.jpg|.*\.gif|.*\.ico>')
def server_static(filename):
    """定义/assets/下的静态(css,js,图片)资源路径"""
    print(assets_path+'\\'+filename)
    return static_file(filename, root=assets_path)


@get("/")
def index():
	return template("index")
@get("/cmd")
def cmd():
	global groove,user_id
	answer=request.query.userInput
	user_id,reply,groove=robot_airclean(user_id,answer,groove)

	return reply
run(host='localhost',port=8080)