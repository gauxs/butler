import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import json
class MainHandler(tornado.web.RequestHandler):
    def get(self):                                                                                                                                                                                            
        loader = tornado.template.Loader(".")                                                                                                                                                                  
        self.write(loader.load("index.html").generate())    

class WSHandler(tornado.websocket.WebSocketHandler):                                                                                                                                                      
    def open(self):                                                                                                                                                                                           
        print 'connection opened...'                                                                                                                                                                            
        self.write_message("The server says: 'Hello'. Connection was accepted.")                                                                                                                                                                                                                                                                                                                                      
        
    def on_message(self, message):                                                                                                                                                                            
        self.write_message("The server says: " + message + " back at you")                                                                                                                                      
        print 'received:', message                                                                                                                                                                              
        print 'JSON:', json.loads(message)                                                                                                                                                                                                                                                                                                                                                                            
        
    def on_close(self):                                                                                                                                                                                       
        print 'connection closed...'                                                                                                                                                                                                                                                                                                                                                                                
        application = tornado.web.Application([
            (r'/butler', WSHandler),                                                                                                                                                                                
            (r'/', MainHandler),                                                                                                                                                                                    
            (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),                                                                                                                                   
            ])                                                                                                                                                                                                                                                                                                                                                                                                              
    
    if __name__ == "__main__":                                                                                                                                                                                
        application.listen(3000)                                                                                                                                                                                
        tornado.ioloop.IOLoop.instance().start()
