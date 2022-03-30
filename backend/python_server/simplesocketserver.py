import json
import redis
import operator
import tornado.web
import collections
import tornado.ioloop
import tornado.websocket
import tornado.template


class MainHandler(tornado.web.RequestHandler):
    def get(self):                                                                                                                                                                                            
        loader = tornado.template.Loader(".")                                                                                                                                                                  
        self.write(loader.load("index.html").generate())    

class WSHandler(tornado.websocket.WebSocketHandler):                                                                                                                                                      
    def get_request_from_user():
        # creating dummy req
        temp = {'Bread': 1, 'Rice': 1, 'Curry': 1}
        return temp


    def get_min_price_values(self):
        conn = redis.Redis('localhost', port=6379)
        rest_details = json.loads(conn.hget('/Butler/FoodPanda', 'value'))

        min_value_rest = {}
        for rname, value in rest_details.items():
            #print rname, value
            if 'North Indian' in value['cuisine'].keys():
                north_cuisine = value['cuisine']['North Indian']
                north_indian = {}
                for ctype in ('Bread', 'Rice', 'Curry'):
                    if ctype in north_cuisine.keys():
                        dish_type = north_cuisine[ctype]
                        # sort dict [some value not able to sort, need to check again]
                        dish_type = sorted(north_cuisine[ctype].items(), key=operator.itemgetter(1))
                        #print bread
                        for cname, cprice in dish_type:
                            #print cname, cprice
                            north_indian[ctype] = {cname: cprice}
                            break
 
                min_value_rest[rname] = north_indian

        return min_value_rest

    def response_from_server (self, min_value_rest, user_data):
        response_dict = {}
        for rname, rvalue in min_value_rest.items():
            local_dict = {}
            total_amount = 0
            for utype, uval in user_data.items():
                if uval != 0 and utype in rvalue.keys():
                    local_dict.update(rvalue[utype])
                    for k in rvalue[utype].keys():
                        price = rvalue[utype][k]
                        if price:
                            price = float(price.strip('Rs.'))
                            total_amount = total_amount +  price * float(uval)

            local_dict.update({'Total': total_amount})
            response_dict[rname] = local_dict

        #print response_dict
        return response_dict

    def open(self):                                                                                                                                                                                           
        print 'connection opened...'                                                                                                                                                                            
        #self.write_message("The server says: 'Hello'. Connection was accepted.")                                                                                                                                                                                                                                                                                                                                      
        
    def on_message(self, message):                                                                                                                                                                            
        user_data = json.loads(message)
        # Find all minimum value resturant
        min_value_rest = self.get_min_price_values()
        #print min_value_rest
        # send result
        response_dict = self.response_from_server(min_value_rest, user_data)
        #self.write_message("The server says: " + message + " back at you") 
        self.write_message(json.dumps(response_dict))                                                                                                                                     
        print 'received:', message                                                                                                                                                                              
        print 'JSON:', json.loads(message)
        print 'reply', json.dumps(response_dict)                                                                                                                                                                                                                                                                                                                                                                           
        
    def on_close(self):                                                                                                                                                                                       
        print 'connection closed...'                                                                                                                                                                                                                                                                                                                                                                                
application = tornado.web.Application([(r'/butler', WSHandler),(r'/', MainHandler),(r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),])                                                                                                                                                                                                                                                                                                                                                                                                              
    
if __name__ == "__main__":                                                                                                                                                                                
    application.listen(3000)                                                                                                                                                                                
    tornado.ioloop.IOLoop.instance().start()

