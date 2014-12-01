# coding: utf-8

import os
import string
import urllib2
import StringIO
import logging

import config

def download_file(file_url, file_name, in_file_size):
    try:                 
        download_size = 0
        content_length = 0
        file_size = 0
        if(config.ENABLE_PROXY == 1):
            proxy_handler = urllib2.ProxyHandler({"http" : config.HTTP_PROXY})
            opener = urllib2.build_opener(proxy_handler)
            urllib2.install_opener(opener)
        request = urllib2.Request(file_url) 
        response = urllib2.urlopen(request, timeout=config.DOWNLOAD_TIMEOUT)   
        str_content_length = dict(response.headers).get('content-length', 0)
        content_length = string.atoi(str_content_length, 10)
        f = open(file_name, 'wb')        
        data = response.read() 
        f.write(data)
        download_size = len(data)           
        f.close() 
               
        file_size = os.path.getsize(file_name)        
        logging.info( 'in_file_size=[%d], content_length=[%d], download_size=[%d], file_size=[%d], url=[%s], file=[%s]' % \
                      (in_file_size, content_length, download_size, file_size, file_url, file_name))
        if(in_file_size != 0 and in_file_size != content_length):
            logging.warn("content_length error, content_length[%d] != in_file_size[%d], url=[%s], file=[%s]" % \
            (content_length, in_file_size, file_url, file_name))
            return False 
        if(download_size != content_length):
            logging.warn("file download error, download_size[%d] != content_length[%d], url=[%s], file=[%s]" % \
            (download_size, content_length, file_url, file_name))
            return False 
        if(file_size != download_size):
            logging.warn("file download error, file_size[%d] != download_size[%d], url=[%s], file=[%s]" % \
            (file_size, download_size, file_url, file_name))
            return False
        
    except Exception, e:
        logging.error('file download error, hints=[%s], url=[%s], file=[%s]' %(e, file_url, file_name))
        return False
    return True


def download_file_retry(file_url, file_name, retry_count, file_size):
    retry_num = 0
    while(download_file(file_url, file_name, file_size) == False):        
        #logging.warn('file download failed, index=[%d@%d], url=[%s], file=[%s]' % (retry_num, retry_count, file_url, file_name))
        retry_num = retry_num + 1
        if(retry_num >= retry_count):
            return False
    return True


def download_memory(file_url, in_file_size):
    file_content = StringIO.StringIO()
    try:       
        download_size = 0
        if(config.ENABLE_PROXY == 1):
            proxy_handler = urllib2.ProxyHandler({"http" : config.HTTP_PROXY})
            opener = urllib2.build_opener(proxy_handler)
            urllib2.install_opener(opener)
        request = urllib2.Request(file_url) 
        response = urllib2.urlopen(request, timeout=config.DOWNLOAD_TIMEOUT)   
        content_length = 0
        header_dict = dict(response.headers)
        if(header_dict.has_key('content-length')):
            str_content_length = header_dict.get('content-length', 0)        
            content_length = string.atoi(str_content_length, 10)        
        data = response.read()        
        file_content.write(data)
        download_size = len(data) 
        logging.info( 'in_file_size=[%d], content_length=[%d], download_size=[%d], url=[%s]' % \
                      (in_file_size, content_length, download_size, file_url))        
        if(in_file_size != 0 and content_length != 0 and in_file_size != content_length):
            logging.warn("content_length error, content_length[%d] != in_file_size[%d], url=[%s]" % \
            (content_length, in_file_size, file_url))
            return (False, None) 
        if(content_length != 0 and download_size != content_length):
            logging.warn("file download error, download_size[%d] != content_length[%d], url=[%s]" % \
            (download_size, content_length, file_url))
            return (False, None)         
    except Exception, e:
        logging.error('file download error, hints=[%s], url=[%s]' %(e, file_url))
        return (False, None)
    return (True, file_content)


def download_memory_retry(file_url, retry_count, file_size):
    retry_num = 0
    while(1):        
        (ret, m3u8_content) = download_memory(file_url, file_size)
        if(ret == False):
            logging.warn('file download to memory failed, index=[%d@%d], url=[%s]' % (retry_num, retry_count, file_url))
            retry_num = retry_num + 1
            if(retry_num >= retry_count):
                return (False, None)
        else:
            return (True, m3u8_content)

    

