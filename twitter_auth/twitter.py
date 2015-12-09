import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.auth
import tornado.gen
import os.path

from tornado.options import define,options
define('port',default=8088, help='run on the given port', type=int)

class TwitterHandler(tornado.web.RequestHandler, tornado.auth.TwitterMixin):
	@tornado.gen.coroutine
	def get(self):
		oAuthToken = self.get_secure_cookie('oauth_token')
		oAuthSecret = self.get_secure_cookie('oauth_secret')
		userID = self.get_secure_cookie('user_id')
		
		if oAuthToken and oAuthSecret:
			accessToken = {
				'key':oAuthToken,
				'secret':oAuthSecret
			}
			user = yield self.twitter_request(
				'/users/show',
				access_token=accessToken,
				user_id=userID,	
			)
			if not user:
				self.clear_all_cookies()
				raise tornado.web.HTTPError(500,'Could not retrieve user information')
			self.render('home.html',user=user)
		else:
			print 'need authorize'
			yield self.authorize_redirect()
			
class LoginHandler(tornado.web.RequestHandler,tornado.auth.TwitterMixin):
	@tornado.gen.coroutine
	def get(self):
		print 'hi Twitter!'
		if self.get_argument('oauth_token',None):
			user = yield self.get_authenticated_user()
			if not user:
				self.clear_all_cookies()
				raise tornado.web.HTTPError(500,'Twitter authentication failed')
			self.set_secure_cookie('user_id',str(user['id']))
			self.set_secure_cookie('oauth_token',user['access_token']['key'])
			self.set_secure_cookie('oauth_secret',user['access_token']['secret'])
			self.redirect('/')
		else:
			yield self.authorize_redirect()


class LogoutHandler(tornado.web.RequestHandler):
	def get(self):
		self.clear_all_cookies()
		self.render('logout.html')


class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r'/',TwitterHandler),
			(r'/login',LoginHandler),
			(r'/logout',LogoutHandler)
		]
		settings = {
			# mask for security
			'twitter_consumer_key':'Na3n........C5M0WIPND',
			'twitter_consumer_secret':'3HW2TFHFls...................XrbqUMmIFcPzU93xa',
			'cookie_secret':'NTliOTY5NzJkYTVlMTU0OTAwMTdlNjgzMTA5M2U3OGQ5NDIxZmU4Mg==',
			'template_path': os.path.join(os.path.dirname(__file__),'templates'),
			'debug':True,
		}
		tornado.web.Application.__init__(self,handlers,**settings)

if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = Application()
	httpserver = tornado.httpserver.HTTPServer(app)
	httpserver.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
