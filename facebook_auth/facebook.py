from tornado.web import RequestHandler, authenticated, Application, UIModule
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line, parse_config_file
from tornado.auth import FacebookGraphMixin
import tornado.gen
from tornado.escape import json_encode, json_decode
from datetime import datetime

define('port',default=8088,type=int, help='run on the given port')
define('debug',default=False,type=bool,help='run on the debug mode')
define('facebook_api_key',type=str,help='your facebook application api key')
define('facebook_app_secret',type='str',help='your facebook application app secret')

class BaseHandler(RequestHandler):
	COOKIE_NAME = 'fbdemo_user'
	def get_current_user(self):
		user_json = self.get_secure_cookie(COOKIE_NAME)
		if user_json:
			return json_decode(user_json)
		else:
			return None

class MainHandler(BaseHandler, FacebookGraphMixin):
	@authenticated
	@tornado.gen.coroutine
	def get(self):
		myfeed = yield self.facebook_request(
			'/me/feed/',
			access_token=self.current_user['access_token'])
		if not myfeed:
			self.redirect('/auth/login/')
			return
		else:
			self.render('home.html',feed=myfeed['data'] if myfeed else [],name=self.current_user['name'])

class LoginHandler(BaseHandler, FacebookGraphMixin):
	@tornado.gen.coroutine
	def get(self):
		if self.get_argument('code',None):
			user = yield self.get_authenticated_user(
				redirect_uri = '/auth/facebookgraph/',
				client_id = self.settings['facebook_api_key'],
				client_secret = self.settings['facebook_app_secret'],
				code = self.get_argument('code'))
			# save the user as cookie
			self.set_secure_cookie(self.COOKIE_NAME,json_encode(user))
			self.redirect('/')
		else:
			yield self.authorize_redirect()

class LogoutHandler(BaseHandler, FacebookGraphMixin):
	def get(self):
		self.clear_cookie(self.COOKIE_NAME)
		self.render('logout.html')
	
class DemoApplication(Application):
	def __init__(self):
		handlers = [
			(r'/',MainHandler),
			(r'/auth/login/',LoginHandler),
			(r'/auth/logout',LogoutHandler)
		]

		settings = {
			facebook_api_key : options.facebook_api_key,
			facebook_app_secret : options.facebook_app_secret,
			login_url = '/auth/login/',
			cookie_secret = 'NTliOTY5NzJkYTVlMTU0OTAwMTdlNjgzMTA5M2U3OGQ5NDIxZmU3Mg==',
			template_path = os.path.join(os.path.dirname(__file__)+'templates'),
			'ui_modules' : { 'FeedListItem' : FeedListItem},
		}
		super(Application,self).__init__(handlers,**settings)

class FeedListItem(UIModule):
	def render(self,statusItem):
		dateFormatter = lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%S+0000').strftime('%c')
		return self.render_string('entry.html', item=statusItem, format=dateFormatter)

if __name__ == '__main__':
	parse_command_line()
	http_server = HTTPServer(DemoApplication())
	http_server.listen(options.port)
	IOLoop.instance().start()

	
