#encoding=utf-8
'''
This program takes a person standing in front of a green screen
and then removes the background and inserts a new one
'''
print __doc__
import os.path
import re
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from SimpleCV import *
from tornado.options import define, options
define("port", default=18001, help="run on the given port", type=int)
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
             (r"/blue", BlueHandler),
	     ]
        settings = dict(
            #urlcheck_title=u"URL",
            #template_path=os.path.join(os.path.dirname(__file__), "templates"),
            #static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
            ) 
        tornado.web.Application.__init__(self, handlers, **settings)
class BlueHandler(tornado.web.RequestHandler):
    def get(self):
        pic_name = self.get_argument('pic')  	
        bg_name = self.get_argument('bg')
	#pic_name = "/var/web/screen/upload"+ pic_name 
	#bg_name = "/var/web/screen/backgroup "+ bg_name 
	print bg_name,pic_name
	background = Image("/home/justzx/workplace/greenscreen/bg1.jpg")
	greenscreen = Image("/home/justzx/workplace/greenscreen/ghost.png")		
        mask = greenscreen.hueDistance(color=Color.GREEN).binarize()
	result = (greenscreen - mask) + (background - mask.invert())
	result.save("/home/justzx/workplace/greenscreen/result.png")
        print type(result),result
        #self.render("index.html",info=info)
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
