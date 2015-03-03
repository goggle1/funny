#coding: utf-8
import ip_db

def ip_section_read_line(one_line, line_index):
    #print "index=%d, line=[%s]" % (line_index, one_line)
    the_parts = one_line.split(';')
    one_ip_section = ip_db.IpSection(the_parts[0], the_parts[1])
    return one_ip_section
    

def ip_section_check(file_name):
    ip_section_list = []
    
    ip_file = open(file_name)
    line_index = 0    
    while 1:        
        one_line = ip_file.readline()
        if not one_line:
            break
        one_line = one_line.strip("\n")
        one_line = one_line.strip("\r")
        if(len(one_line)==0):
            continue
        one_ip_section = ip_section_read_line(one_line, line_index)
        ip_section_list.append(one_ip_section)
        line_index += 1
        

def ip_section_sort(file_name):
    ip_section_list = []
    
    ip_file = open(file_name)
    line_index = 0    
    while 1:        
        one_line = ip_file.readline()
        if not one_line:
            break
        one_line = one_line.strip("\n")
        one_line = one_line.strip("\r")
        if(len(one_line)==0):
            continue
        one_ip_section = ip_section_read_line(one_line, line_index)
        ip_section_list.append(one_ip_section)
        line_index += 1
        
    ip_section_list.sort(cmp=None, key=lambda x:x.ip_start, reverse=False)
    for one_ip_section in ip_section_list:
        print "%s;%s" % (one_ip_section.ip_section, one_ip_section.area)
        
        
                
def ip_section_overlap(file_name):
    ip_section_list = []
    
    ip_file = open(file_name)
    line_index = 0    
    while 1:        
        one_line = ip_file.readline()
        if not one_line:
            break
        one_line = one_line.strip("\n")
        one_line = one_line.strip("\r")
        if(len(one_line)==0):
            continue
        one_ip_section = ip_section_read_line(one_line, line_index)
        ip_section_list.append(one_ip_section)
        line_index += 1
        
    ip_section_list.sort(cmp=None, key=lambda x:x.ip_start, reverse=False)
    ip_section_index = 1
    last_ip_section = None
    for one_ip_section in ip_section_list:        
        print "index=%d, ip_section=[%s;%s;%s-%s]" % (ip_section_index, one_ip_section.ip_section, one_ip_section.area, one_ip_section.str_ip_start, one_ip_section.str_ip_stop)
        if(last_ip_section != None):
            if(one_ip_section.ip_start <= last_ip_section.ip_stop):
                if(last_ip_section.ip_start  <= one_ip_section.ip_start and last_ip_section.ip_stop >= one_ip_section.ip_stop):
                    print "overlap[inner]: last_ip_section=[%s;%s;%s-%s], this_ip_section=[%s;%s;%s-%s]" % \
                    (last_ip_section.ip_section, last_ip_section.area, last_ip_section.str_ip_start, last_ip_section.str_ip_stop, one_ip_section.ip_section, one_ip_section.area, one_ip_section.str_ip_start, one_ip_section.str_ip_stop)
                elif(last_ip_section.ip_start  >= one_ip_section.ip_start and last_ip_section.ip_stop <= one_ip_section.ip_stop):
                    print "overlap[contain]: last_ip_section=[%s;%s;%s-%s], this_ip_section=[%s;%s;%s-%s]" % \
                    (last_ip_section.ip_section, last_ip_section.area, last_ip_section.str_ip_start, last_ip_section.str_ip_stop, one_ip_section.ip_section, one_ip_section.area, one_ip_section.str_ip_start, one_ip_section.str_ip_stop)
                else:
                    print "overlap[intersect]: last_ip_section=[%s;%s;%s-%s], this_ip_section=[%s;%s;%s-%s]" % \
                    (last_ip_section.ip_section, last_ip_section.area, last_ip_section.str_ip_start, last_ip_section.str_ip_stop, one_ip_section.ip_section, one_ip_section.area, one_ip_section.str_ip_start, one_ip_section.str_ip_stop)
        last_ip_section = one_ip_section
        ip_section_index += 1
                
    
if __name__ == "__main__":
    #file_name = "ip_lib.1"
    #ip_section_check(file_name)
    #file_name = "ip_lib.1"    
    #ip_section_sort(file_name)
    file_name = "ip_lib.sort"
    ip_section_overlap(file_name)
    
