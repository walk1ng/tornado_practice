import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os.path

from tornado.options import define,options
define('port',default=8000,type=int,help='run on given port')

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html',header_text="my great header",footer_text="my great footer")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/',IndexHandler)],
        template_path = os.path.join(os.path.dirname(__file__),"templates"),
        debug=True)
    httpserver = tornado.httpserver.HTTPServer(app)
    httpserver.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
