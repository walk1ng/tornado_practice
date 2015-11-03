import tornado.web                       
import tornado.httpserver                                                                
import tornado.ioloop                                                                    
import tornado.options                                                                   
import os.path                                                                           
                                                                                         
from tornado.options import define, options                                              
define("port", default=8000, help="run on the given port", type=int)

class RecommendedHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('recommended.html',
			page_title = "Burt's books | Recommended reading",
			books = [
				{
					"title": "Tornado Web",
					"author": "Wei Li",
					"details": "This fascinating book demonstrates how you "
						"can build web applications to mine the enormous amount of data created by people "
						"on the Internet. With the sophisticated algorithms in this book, you can write "
						"smart programs to access interesting datasets from other web sites, collect data "
						"from users of your own applications, and analyze and understand the data once "
						"you've found it."
				},
				{
                                        "title": "RESTful service",
                                        "author": "Wei Li",
                                        "details": "This fascinating book demonstrates how you "
					"can build web applications to mine the enormous amount of data created by people "
					"on the Internet. With the sophisticated algorithms in this book, you can write "
					"smart programs to access interesting datasets from other web sites, collect data "
					"from users of your own applications, and analyze and understand the data once "
					"you've found it."
				}
			]
		)

class BookModule(tornado.web.UIModule):
	def render(self,book):
		return self.render_string('modules/book.html',book=book)

if __name__ == '__main__':                                                               
	tornado.options.parse_command_line()                                                 
	app = tornado.web.Application(                                                       
        handlers=[(r'/', RecommendedHandler)],                                                 
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
	static_path = os.path.join(os.path.dirname(__file__),"static"),              
        ui_modules={'Book': BookModule},
	debug=True                                         
    	)                                                                                    
    	server = tornado.httpserver.HTTPServer(app)                                          
    	server.listen(options.port)                                                          
	tornado.ioloop.IOLoop.instance().start() 
