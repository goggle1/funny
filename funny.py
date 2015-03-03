# coding: utf-8
import os
import json
import logging
import tornado.ioloop
import tornado.web

import config
import ip_db
import utils

g_ip_db = None

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, I am funny.<p>\n")
        
class LiveWinHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./live/win.html")
        
        
class LiveIosHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./live/ios.html")


class LiveJsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./live/jquery-1.10.1.min.js")
        
                
class LiveChannelsHandler(tornado.web.RequestHandler):
    def get(self):
        # http://223.99.189.101:8010/chnList/
        channels_url = "http://223.99.189.101:8010/chnList/"
        (ret, channels_content) = utils.download_memory(channels_url, 0)
        if(ret == False):
            self.write("")
        channels_content.seek(0)
        channels_data = channels_content.read()
        self.write(channels_data)
        

class IpCountHandler(tornado.web.RequestHandler):
    def get(self):
        self.handle()
        
    def post(self):
        self.handle()
        
    def handle(self):
        ip_count = len(g_ip_db.ip_list)
        logging.info("IpCountHandler: ip_count=[%d]" % (ip_count))
        response_data = {"count":ip_count, "result":1}
        json_data = json.dumps(response_data)        
        self.write(json_data)
        return True
    
    
class IpQueryHandler(tornado.web.RequestHandler):
    def get(self):
        self.handle()
        
    def post(self):
        self.handle()
        
    def prompt(self):
        self.write('<html><body><form action="/ip_query" method="post">'
                   'ip(db_iqiyi): <input type="text" name="ip">'
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
    
class IpQuery2Handler(tornado.web.RequestHandler):
    def get(self):
        self.handle()
        
    def post(self):
        self.handle()
        
    def prompt(self):
        self.write('<html><body><form action="/ip_query2" method="post">'
                   'ip(db_lanmu): <input type="text" name="ip">'
                   '<input type="submit" value="query">'
                   '</form></body></html>')
        
    def handle(self):        
        param_ip = self.get_argument("ip", "null")   
        if(cmp(param_ip, "null") == 0):
            return self.prompt()     
        (result, num_ip, ip_section, area) = g_ip_db2.query(param_ip)
        logging.info("IpQueryHandler received: ip_db=[%s], result=[%s], num_ip=%d[0x%08X], ip_section=[%s], area=[%s]" % \
                     (param_ip, result, num_ip, num_ip, ip_section, area))
        response_data = {"ip":param_ip, "result":result, "num":num_ip, "section":ip_section, "area":area}
        json_data = json.dumps(response_data)        
        self.write(json_data)
        return True


class IpTrans1Handler(tornado.web.RequestHandler):
    def get(self):
        self.handle()
        
    def post(self):
        self.handle()
        
    def prompt(self):
        self.write('<html><body><form action="/ip_trans1" method="post">'
                   'ip1-ip2: <input type="text" name="ip1_ip2">'
                   '<input type="submit" value="transform">'
                   '</form></body></html>')
        
    def handle(self):        
        param_ip1_ip2 = self.get_argument("ip1_ip2", "null")   
        if(cmp(param_ip1_ip2, "null") == 0):
            return self.prompt()     
        (result, ip_sections) = ip_db.ip_trans_1(param_ip1_ip2)        
        response_data = {"ip1_ip2":param_ip1_ip2, "result":result, "num":len(ip_sections), "sections":[]}
        for one_section in ip_sections:
            response_data["sections"].append(one_section)
        json_data = json.dumps(response_data)     
        logging.info("IpTrans1Handler received: param_ip1_ip2=[%s], result=[%d], num=%d" % (param_ip1_ip2, result, len(ip_sections)))
        logging.info(json_data)  
        self.write(json_data)
        return True

    
class IpTrans2Handler(tornado.web.RequestHandler):
    def get(self):
        self.handle()
        
    def post(self):
        self.handle()
        
    def prompt(self):
        self.write('<html><body><form action="/ip_trans2" method="post">'
                   'ip1/mask: <input type="text" name="ip1_mask">'
                   '<input type="submit" value="transform">'
                   '</form></body></html>')
        
    def handle(self):        
        param_ip1_mask = self.get_argument("ip1_mask", "null")   
        if(cmp(param_ip1_mask, "null") == 0):
            return self.prompt()     
        (result, ip_start, ip_stop) = ip_db.ip_trans2(param_ip1_mask)  
        str_ip1_ip2 = "%s-%s" % (ip_start, ip_stop)      
        response_data = {"ip1/mask":param_ip1_mask, "result":result, "ip1-ip2":str_ip1_ip2}        
        json_data = json.dumps(response_data)     
        logging.info("IpTrans2Handler received: param_ip1_mask=[%s], result=[%s], ip1-ip2=[%s]" % (param_ip1_mask, result, str_ip1_ip2))
        logging.info(json_data)  
        self.write(json_data)
        return True
    
                    
settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    #"cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    #"login_url": "/login",
    #"xsrf_cookies": True,
}

application = tornado.web.Application([
    (r"/",                          MainHandler),
    (r"/static/.*",                    tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
    #(r"/.*\.html",                  tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
    (r"/live/win",                  LiveWinHandler), 
    (r"/live/ios",                  LiveIosHandler),    
    (r"/live/channels",             LiveChannelsHandler),
    (r"/ip_count",                  IpCountHandler),
    (r"/ip_query",                  IpQueryHandler),
    (r"/ip_query2",                 IpQuery2Handler),
    (r"/ip_trans1",                 IpTrans1Handler),
    (r"/ip_trans2",                 IpTrans2Handler),
    #(r"/ip_section_combine",        IpSectionCombineHandler),
], **settings)

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
    
    file_name = "./ip_lib.list.default.20141219"
    g_ip_db2 = ip_db.IpDb()
    g_ip_db2.load(file_name)
    
    logging.info('listen @%d ......' % (config.LISTEN_PORT))
    application.listen(config.LISTEN_PORT)
    tornado.ioloop.IOLoop.instance().start()