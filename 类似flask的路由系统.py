class WSGIapp(object):
    def __init__(self):
        self.routes = {}

    def route(self,path=None):#带参数的装饰器
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator

    def __call__(self,environ,start_response):
        path = environ['PATH_INFO']
        if path in self.routes:
            status = '200 OK'
            response_headers = [('Content-Type','text/plain')]
            start_response(status,response_headers)
            return self.routes[path]()
        else:
            status = '404 Not Found'
            response_headers = [('Content-Type','text/plain')]
            start_response(status,response_headers)
            return '404 Not Found!'

app = WSGIapp()

@app.route('/')
def index():
    return ['index']

@app.route('/hello')
def hello():
    return ['hello world']

from wsgiref.simple_server import make_server
httpd = make_server('',8888,app)
httpd.serve_forever()

"""
在浏览器上，输入127.0.0.1:8888---输出index内容
在浏览器上，输入127.0.0.1:8888/hello---输出hello word内容
"""
