import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os.path

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class HelloModule(tornado.web.UIModule):
    def render(self):
	return '<h1>Message comes from Hello module!</h1>'

class HelloHandler(tornado.web.RequestHandler):
    def get(self):
	#self.render('hello.html')
	self.write('nihao')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
	hanlders=[(r'/',HelloHandler)],
	template_path = os.path.join(os.path.dirname(__file__),'templates'),
    )
    httpserver = tornado.httpserver.HTTPServer(app)
    httpserver.listen(options.port)
    tornado.ioloop.IOLoop.instance().start() 
