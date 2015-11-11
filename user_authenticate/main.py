import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
import os.path

from tornado.options import define, options
define('port', default=8000, help='run on the given port',type=int)

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie('username')

class LoginHandler(BaseHandler):
	def get(self):
		if not self.current_user:
			self.render('login.html')
		else:
			self.redirect('/')
	def post(self):
		self.set_secure_cookie('username',self.get_argument('username'))
		print 'debug info:',self.current_user
		self.redirect('/')

class WelcomeHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.render('index.html',user=self.current_user)

class LogoutHandler(BaseHandler):
	def get(self):
		self.clear_cookie('username')
		self.redirect('/')

class TestHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('a.html')

if __name__ == "__main__":
	tornado.options.parse_command_line()
	settings = {
		'template_path': os.path.join(os.path.dirname(__file__),'templates'),
		'cookie_secret':'bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89X=',
		'xsrf_cookies':True,
		'login_url':'/login',
		'debug': True
	}
	app = tornado.web.Application([
		(r'/',WelcomeHandler),
		(r'/login',LoginHandler),
		(r'/logout',LogoutHandler),
		(r'/test',TestHandler)
	],**settings)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
