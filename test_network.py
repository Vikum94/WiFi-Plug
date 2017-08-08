import nmap 

nm = nmap.PortScanner() 

# nm.scan(hosts='192.168.1.0/24', arguments='-n -sP -PE -PA21,23,80,3389')


# hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
# for host, status in hosts_list:
# 	#print('Host : %s (%s)' % (host, nm[host].hostname()))
# 	#print('Product : %s ') % (nm[host].product)
# 	print('{0}:{1}'.format(host, status))

# for host in nm.all_hosts():
# 	print nm[host].hostname()

# print(nm.csv())

cidr2 = '192.168.1.0/24'
a=nm.scan(hosts=cidr2, arguments='-sP') 
path = 'devices.txt'

file=open(path,'w')

for k,v in a['scan'].iteritems(): 
    if str(v['status']['state']) == 'up':
        #print str(v)
        
        try:
        	if 'Tp-link Technologies' in str(v['vendor']):
        		file.write(str(v['addresses']['ipv4']) + ' ' + str(v['vendor']) + '\n')    
        	print str(v['addresses']['ipv4']) + ' => ' + str(v['addresses']['mac'] + str(v['vendor']))
        except: print str(v['addresses']['ipv4'])

file.close()