# coding: utf-8
import json
import logging
import tornado.ioloop
import tornado.web

import config
import ip_db

g_ip_db = None

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, I am funny.<p>\n")
        

class IpQueryHandler(tornado.web.RequestHandler):
    def get(self):
        self.handle()
        
    def post(self):
        self.handle()
        
    def prompt(self):
        self.write('<html><body><form action="/ip_query" method="post">'
                   'ip: <input type="text" name="ip">'
                   '<input type="submit" value="query">'
                   '</form></body></html>')
        
    def handle(self):        
        param_ip = self.get_argument("ip", "null")   
        if(cmp(param_ip, "null") == 0):
            return self.prompt()     
        (result, num_ip, ip_section, area) = g_ip_db.query(param_ip)
        logging.info("IpQueryHandler received: ip_db=[%s], result=[%s], num_ip=%d[0x%08X], ip_section=[%s], area=[%s]" % \
                     (param_ip, result, num_ip, num_ip, ip_section, area))
        response_data = {"ip":param_ip, "result":result, "num":num_ip, "section":ip_section, "area":area}
        json_data = json.dumps(response_data)        
        self.write(json_data)
        return True
                

application = tornado.web.Application([
    (r"/",                          MainHandler),    
    (r"/ip_query",                  IpQueryHandler),
])

if __name__ == "__main__":    
    logging.basicConfig(filename=config.LOG_FILENAME, level=logging.INFO)
    '''
    console = logging.StreamHandler()  
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console) 
    '''    
    
    file_name = "./ip_zone.txt"
    g_ip_db = ip_db.IpDb()
    g_ip_db.load(file_name)
    
    logging.info('listen @%d ......' % (config.LISTEN_PORT))
    application.listen(config.LISTEN_PORT)
    tornado.ioloop.IOLoop.instance().start()