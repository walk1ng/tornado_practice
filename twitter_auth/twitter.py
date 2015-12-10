"""
  Create a file called "secrets.cfg" and put your consumer key and
     secret (which Twitter gives you when you register an app) in it:
       twitter_consumer_key = 'asdf1234'
       twitter_consumer_secret = 'qwer5678'
     (you could also generate a random value for "cookie_secret" and put it
     in the same file, although it's not necessary to run this demo)
"""
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.auth
import tornado.gen
import os.path
from tornado.escape import json_decode, json_encode
import logging

from tornado.options import define,options
define('port',default=8088, help='run on the given port', type=int)
define('config_file',default='secrets.cfg',help='filename for addtional configurations')
define('debug',default=False,help='run app on debug mode',type=bool,group='application')
define('twitter_consumer_key',type=str,group='application')
define('twitter_consumer_secret',type=str,group='application')
define('cookie_secret',type=str,group='application')

class BaseHandler(tornado.web.RequestHandler):
	COOKIE_NAME = 'demo_user'
	def get_current_user(self):
		user_json = self.get_secure_cookie(self.COOKIE_NAME)
		if not user_json:
			return None
		else:
			return json_decode(user_json)

class TwitterHandler(BaseHandler, tornado.auth.TwitterMixin):
	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self):	
		user = yield self.twitter_request(
			'/users/show',
			access_token=self.current_user['access_token'],
			user_id = self.current_user['id']
		)
		if not user:
			self.clear_all_cookies()
			raise tornado.web.HTTPError(500,'Could not retrieve user information')
		self.render('home.html',user=user)
			
class LoginHandler(BaseHandler,tornado.auth.TwitterMixin):
	@tornado.gen.coroutine
	def get(self):
		if self.get_argument('oauth_token',None):
			user = yield self.get_authenticated_user()
			if not user:
				self.clear_all_cookies()
				raise tornado.web.HTTPError(500,'Twitter authentication failed')
			self.set_secure_cookie(self.COOKIE_NAME,json_encode(user))
			self.redirect('/')
		else:
			yield self.authorize_redirect()

class LogoutHandler(BaseHandler):
	def get(self):
		self.clear_cookie(self.COOKIE_NAME)
		self.render('logout.html')


class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r'/',TwitterHandler),
			(r'/login',LoginHandler),
			(r'/logout',LogoutHandler)
		]
		tornado.web.Application.__init__(self,handlers,template_path=os.path.join(os.path.dirname(__file__),'templates'),login_url='/login',**options.group_dict('application'))

if __name__ == "__main__":
	tornado.options.parse_command_line()
	tornado.options.parse_config_file(options.config_file)
	app = Application()
	httpserver = tornado.httpserver.HTTPServer(app)
	httpserver.listen(options.port)
	logging.info('app run on the port: %d' % options.port )
	tornado.ioloop.IOLoop.instance().start()
