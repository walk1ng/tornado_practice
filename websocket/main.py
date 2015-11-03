import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.websocket

from tornado.options import define,options

define('port',type=int,help='run on the given port',default=8000)

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello, this is a websocket tester!")

class ChatSocketHandler(tornado.websocket.WebSocketHandler):
	handlers = set()
	def send_message(self,message):
		for h in ChatSocketHandler.handlers:
			h.write_message('[serv resp]:'+ message)
	def open(self):
		print 'A user join.'
		ChatSocketHandler.handlers.add(self)
		self.send_message('Server: A new user has entered the chat room.')

	def on_close(self):
		print 'A user left.'
		ChatSocketHandler.handlers.remove(self)
		self.send_message("Server: A user has left the chat room.")

	def on_message(self,message):
		print 'Server: %s' % message
		self.send_message(message)
	

if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(handlers=[(r'/',MainHandler), (r'/socket',ChatSocketHandler)],debug=True)
	httpserver = tornado.httpserver.HTTPServer(app)
	httpserver.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
