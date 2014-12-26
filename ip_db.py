# coding: utf-8
import sys
import string
import struct
import socket
import logging

def check_ip(ipaddr):
    addr_list = ipaddr.strip().split('.')  
    if len(addr_list) != 4:  
        return False
    num_list = [0, 0, 0, 0]
    for i in range(4): 
        '''
        try: 
            addr_list[i]=int(addr_list[i]) 
        except:
            return False
        '''
        if(addr_list[i].isdigit()):
            pass
        else:
            return False
        num_list[i] = string.atoi(addr_list[i])
        if num_list[i]<=255 and num_list[i]>=0: 
            pass
        else:
            return False
    return True


def check_mask(the_mask):     
    if the_mask.isdigit() == False:  
        return False
    num_mask = string.atoi(the_mask)
    if(num_mask < 0):
        return False
    if(num_mask > 32):
        return False
    return True


class IpMask:
    def __init__(self, ip_start, mask_num):
        self.ip_start = ip_start
        self.mask_num = mask_num
        num_remainder = 32-self.mask_num        
        ip_remainder = 0
        for index in range(num_remainder):
            ip_remainder = ip_remainder | 1 << index
        self.ip_stop = self.ip_start + ip_remainder
        self.str_ip_start = socket.inet_ntoa(struct.pack('I',socket.htonl(self.ip_start))) 
        self.str_ip_stop  = socket.inet_ntoa(struct.pack('I',socket.htonl(self.ip_stop))) 
    
    def reset(self, ip_start):
        self.ip_start = ip_start        
        num_remainder = 32-self.mask_num        
        ip_remainder = 0
        for index in range(num_remainder):
            ip_remainder = ip_remainder | 1 << index
        self.ip_stop = self.ip_start + ip_remainder
        self.str_ip_start = socket.inet_ntoa(struct.pack('I',socket.htonl(self.ip_start))) 
        self.str_ip_stop  = socket.inet_ntoa(struct.pack('I',socket.htonl(self.ip_stop)))
        
     
def ip_trans1(ip1_ip2):    
    the_parts = ip1_ip2.split('-')
    if(len(the_parts) < 2):
        return (0, [])
    ip1 = the_parts[0]
    ip2 = the_parts[1]
    if(check_ip(ip1) == False):
        return (0, [])
    if(check_ip(ip2) == False):
        return (0, [])
    ip_start = socket.ntohl(struct.unpack("I",socket.inet_aton(str(ip1)))[0])
    ip_stop  = socket.ntohl(struct.unpack("I",socket.inet_aton(str(ip2)))[0])
    ip_num   = ip_stop - ip_start + 1    
    ip_num_temp = ip_num
    bits_index = 0    
    ip_section_list = []
    while(ip_num_temp>0):
        if(ip_num_temp&1 == 1):
            one_ip_mask = IpMask(ip_start, (32-bits_index)) 
            ip_section_list.insert(0, one_ip_mask)           
        ip_num_temp = ip_num_temp >> 1
        bits_index += 1
    result_list = []
    ip_section_index = 0
    while(ip_section_index<len(ip_section_list)):
        one_ip_mask = ip_section_list[ip_section_index]
        if(ip_section_index!=0):
            one_ip_mask.reset(ip_section_list[ip_section_index-1].ip_stop + 1)
        one_result = "%s/%d[%s-%s]" % (one_ip_mask.str_ip_start, one_ip_mask.mask_num, one_ip_mask.str_ip_start, one_ip_mask.str_ip_stop)
        result_list.append(one_result)
        ip_section_index += 1
    return (len(result_list), result_list)

 
def ip_trans2(ip1_mask):    
    the_parts = ip1_mask.split('/')
    if(len(the_parts) < 2):
        return (0, "", "")
    the_ip = the_parts[0]
    the_mask = the_parts[1]
    if(check_ip(the_ip) == False):
        return (0, "", "")
    if(check_mask(the_mask) == False):
        return (0, "", "")
    num_mask = string.atoi(the_mask)
    num_remainder = 32-num_mask        
    ip_remainder = 0
    for index in range(num_remainder):
        ip_remainder = ip_remainder | 1 << index
    num_network = 0xFFFFFFFF ^ ip_remainder        
    the_ip_num = socket.ntohl(struct.unpack("I",socket.inet_aton(str(the_ip)))[0])
    ip_start = the_ip_num & num_network
    ip_stop = ip_start + ip_remainder
    str_ip_start = socket.inet_ntoa(struct.pack('I',socket.htonl(ip_start))) 
    str_ip_stop  = socket.inet_ntoa(struct.pack('I',socket.htonl(ip_stop))) 
    return (1, str_ip_start, str_ip_stop)
           

class IpSection:
    def __init__(self, ip_section, area):
        self.ip_section     = ip_section
        self.area           = area
        self.ip_start       = 0
        self.ip_stop        = 0
        self.str_ip_start   = ""
        self.str_ip_stop    = ""
        if(ip_section.find('/') >= 0):
            self.read_ip_mask()
        elif(ip_section.find('-') >= 0):
            self.read_ip_start_stop()
        else:
            logging.info("illegal section=[%s], area=[%s]" % (self.ip_section, self.area))
            print ("illegal section=[%s], area=[%s]" % (self.ip_section, self.area))
            sys.exit(-1)
                     
        
        
    def read_ip_mask(self):
        the_parts = self.ip_section.split('/')
        the_ip = the_parts[0]
        the_mask = the_parts[1]
        num_mask = string.atoi(the_mask)
        num_remainder = 32-num_mask        
        ip_remainder = 0
        for index in range(num_remainder):
            ip_remainder = ip_remainder | 1 << index
        num_network = 0xFFFFFFFF ^ ip_remainder        
        the_ip_num = socket.ntohl(struct.unpack("I",socket.inet_aton(str(the_ip)))[0])
        self.ip_start = the_ip_num & num_network
        self.ip_stop = self.ip_start + ip_remainder
        self.str_ip_start = socket.inet_ntoa(struct.pack('I',socket.htonl(self.ip_start))) 
        self.str_ip_stop  = socket.inet_ntoa(struct.pack('I',socket.htonl(self.ip_stop))) 
        logging.info("ip_str=[%s-%s], section=[%s], area=[%s]" % \
                     (self.str_ip_start, self.str_ip_stop, self.ip_section, self.area))
        print ("ip_str=[%s-%s], section=[%s], area=[%s]" % \
                     (self.str_ip_start, self.str_ip_stop, self.ip_section, self.area))
        
    
    def read_ip_start_stop(self):
        the_parts = self.ip_section.split('-')
        ip1 = the_parts[0]
        ip2 = the_parts[1]
        ip_start = socket.ntohl(struct.unpack("I",socket.inet_aton(str(ip1)))[0])
        ip_stop  = socket.ntohl(struct.unpack("I",socket.inet_aton(str(ip2)))[0])
        self.ip_start = ip_start
        self.ip_stop  = ip_stop
        self.str_ip_start = ip1
        self.str_ip_stop  = ip2
        ip_num   = ip_stop - ip_start + 1    
        ip_num_temp = ip_num
        bits_index = 0    
        ip_section_list = []
        while(ip_num_temp>0):
            if(ip_num_temp&1 == 1):
                one_ip_mask = IpMask(ip_start, (32-bits_index)) 
                ip_section_list.insert(0, one_ip_mask)           
            ip_num_temp = ip_num_temp >> 1
            bits_index += 1
        result_list = []
        ip_section_index = 0
        while(ip_section_index<len(ip_section_list)):
            one_ip_mask = ip_section_list[ip_section_index]
            if(ip_section_index!=0):
                one_ip_mask.reset(ip_section_list[ip_section_index-1].ip_stop + 1)
            one_result = "%s/%d(%s-%s)" % (one_ip_mask.str_ip_start, one_ip_mask.mask_num, one_ip_mask.str_ip_start, one_ip_mask.str_ip_stop)
            result_list.append(one_result)
            ip_section_index += 1
        logging.info("ip_str=[%s-%s], section=[%s], area=[%s]" % \
                     (self.str_ip_start, self.str_ip_stop, str(result_list), self.area))
        print ("ip_str=[%s-%s], section=[%s], area=[%s]" % \
                     (self.str_ip_start, self.str_ip_stop, str(result_list), self.area))

    
class IpDb:
    def __init__(self):
        self.ip_list = []
    
    
    def load(self, file_name):
        the_file = open(file_name)
        while 1:        
            line = the_file.readline()
            if not line:
                break
            line = line.strip("\n")
            line = line.strip("\r")
            if(len(line)==0):
                continue
            self.do_line(line)
            
            
    def do_line(self, line):
        the_parts = line.split(';')
        ip_section = the_parts[0]
        area = the_parts[1]
        one_ip_section = IpSection(ip_section, area)
        self.ip_list.append(one_ip_section)
             
    
    def binary_search(self, num_ip, position_begin, position_end):
        if(position_end < position_begin):
            return None
        position_middle = (position_end + position_begin)/2
        one_ip_section = self.ip_list[position_middle]
        logging.info("binary_search(): num_ip=%d[0x%08X], position=[%d, %d, %d], section=[%s], area=[%s]" % \
                     (num_ip, num_ip, position_begin, position_middle, position_end, one_ip_section.ip_section, one_ip_section.area))
        if(num_ip >= one_ip_section.ip_start and num_ip <= one_ip_section.ip_stop):
            return one_ip_section
        if(num_ip < one_ip_section.ip_start):
            position_end = position_middle - 1
            return self.binary_search(num_ip, position_begin, position_end)
        if(num_ip > one_ip_section.ip_stop):
            position_begin = position_middle + 1
            return self.binary_search(num_ip, position_begin, position_end)
        
    
    def query(self, param_ip):
        ret = check_ip(param_ip)
        if(ret == False):
            return (0, 0, "illegal ip", "no area")
        num_ip = socket.ntohl(struct.unpack("I",socket.inet_aton(str(param_ip)))[0])
        position_begin = 0
        position_end = len(self.ip_list)
        findp = self.binary_search(num_ip, position_begin, position_end)
        if(findp == None):
            return (0, num_ip, "no ip_section", "no area")
        else:
            return (1, num_ip, findp.ip_section, findp.area)
    
    