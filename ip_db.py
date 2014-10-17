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
            

class IpSection:
    def __init__(self, ip_section, area):
        the_parts = ip_section.split('/')
        the_ip = the_parts[0]
        the_mask = the_parts[1]
        num_mask = string.atoi(the_mask)
        num_remainder = 32-num_mask        
        ip_remainder = 0
        for index in range(num_remainder):
            ip_remainder = ip_remainder | 1 << index
        self.ip_section = ip_section
        self.area = area
        self.ip_start = socket.ntohl(struct.unpack("I",socket.inet_aton(str(the_ip)))[0])
        self.ip_stop = self.ip_start + ip_remainder
        logging.info("ip_start=0x%08X, ip_stop=0x%08X, section=[%s], area=[%s]" % (self.ip_start, self.ip_stop, self.ip_section, self.area))
    
    
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
    
    