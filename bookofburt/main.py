import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os.path

from tornado.options import define,options
define('port',default=8000,type=int,help='run on the given port')

class Application(tornado.web.Application):
	def __init__(self):
		hls = [(r'/',IndexHandler)]
		settings = dict(
			template_path = os.path.join(os.path.dirname(__file__),"templates"),
			static_path = os.path.join(os.path.dirname(__file__),'static'),
			debug=True,
		)
		tornado.web.Application.__init__(self,hls,**settings)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html',
			header_text='welcome user!',
			page_title="burt's books")
if __name__ == "__main__":
	tornado.options.parse_command_line()
	httpserver = tornado.httpserver.HTTPServer(Application())
	httpserver.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
