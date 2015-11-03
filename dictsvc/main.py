import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import pymongo

from pymongo import MongoClient
from tornado.options import define,options
define('port',default=8000,type=int,help='run on the given port')

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [(r'/(\w+)',WordHandler)]
		client = MongoClient('localhost',27018)
		self.db = client.testdb
		tornado.web.Application.__init__(self,handlers,debug=True)		

class WordHandler(tornado.web.RequestHandler):
	def get(self,word):
		coll = self.application.db.words
		word_doc = coll.find_one({'word':word})
		if word_doc:
			del word_doc['_id']
			self.write(word_doc)
		else:
			self.set_status(404)
			self.write({'error':'not found'})
	def post(self,word):
		coll = self.application.db.words
		definition = self.get_argument('definition')
		word_doc = coll.find_one({'word':word})
		if word_doc:
			word_doc['definition'] = definition
			coll.save(word_doc)
		else:
			word_doc = {'word':word, 'definition': definition}
			coll.insert(word_doc)
		del word_doc['_id']
		self.write(word_doc)
					

if __name__ == "__main__":
	tornado.options.parse_command_line()
	httpserver = tornado.httpserver.HTTPServer(Application())
	httpserver.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
