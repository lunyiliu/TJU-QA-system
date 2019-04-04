# coding:utf8
import os
import json
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options

from robot import robot_airclean
print('start')

define("port", type=int, default=8000)

print('start')

class InterfaceAir(tornado.web.RequestHandler):  
    def get(self):   
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        print('start')
        user_id = self.get_query_argument('user_id', 'None') 
        print('user_id')
        answer  = self.get_query_argument('answer', 'None')
        print('answer')
        groove = self.get_query_argument('groove', 'None') 
        groove = [int(x) for x in groove.split(',')]
        print('groove:',)
        user_id,reply,groove = robot_airclean(user_id,answer,groove)
        groove = ','.join([str(x) for x in groove])
        try:
            respon = {
                      "status": 1,      
                      "user_id": user_id,
                      "answer": reply,
                      "groove": groove
                      }
        except:
            respon = {
                      "status": 0,      
                       "user_id": user_id,
                      "answer": '抱歉，回答不了',
                      "groove": groove
                      }           
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(respon))
        self.finish()  
 


urls = [

    (r"/aircleaner", InterfaceAir)

]

base_dir = os.path.dirname(__file__)
configs = dict(
    debug=True,
    template_path=os.path.join(base_dir, "templates"),
)


class CustomApplication(tornado.web.Application):
    def __init__(self, urls, configs):
        handlers = urls
        settings = configs
        super(CustomApplication, self).__init__(handlers=handlers, **settings)


def create_app():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(CustomApplication(urls, configs))
    http_server.listen(options.port, "0.0.0.0")
    tornado.ioloop.IOLoop.instance().start()


app = create_app()

if __name__ == "__main__":
    app()
