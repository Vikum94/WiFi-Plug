from pyHS100 import SmartPlug
import nmap
import paho.mqtt.client as mqtt
import Queue
import logging

logging.basicConfig(filename='/home/vikum/wifiplug_log_testing.log',level=logging.DEBUG)

cidr2 = '192.168.1.0/24' #Network address

msgQ = Queue.Queue() #To insert the mqtt commands
host = "192.168.1.182" #Mqtt broker address
topic = 'g1'

dev_path = 'devices.txt'
ips = [] #Ip addresses of all Wi-Fi plugs

def on_connect(client, userdata, flags, rc): #When this cline connect to the broker this method runs
        print("Client Connected "+str(rc))
        client.subscribe(topic)

def on_message(client, userdata, message): #On incomming msg to the subscriberd topic, this method runs
        msg = str(message.payload.decode("utf-8"))
        print("Incomming message", msg)
        global msgQ
        msgQ.put(msg)

def command(message):
	msgList = message.split('_')
	if(msgList[0] == "wifiplug"):
		try:
			if('add' in msgList[1]):
				addNewPlug(int(msgList[2])) 
				return	

			id = int(msgList[1]) - 1
			print ips[id]
			if(msgList[2] == "on"):
				plug = SmartPlug(ips[id])
				print("Current state: %s" % plug.state)
				plug.state = "ON"
				return

			if(msgList[2] == "off"):
				plug = SmartPlug(ips[id])
				print("Current state: %s" % plug.state)
				plug.state = "OFF"
				return

		except ValueError:
			logging.warning('Invalid command: Incorrect id format')
			return
		except Exception as e:
			logging.warning(e)
			return

def addNewPlug(id): #Function to add a new plug
	nm = nmap.PortScanner() #For the Network scan
	inFile = False
	a=nm.scan(hosts=cidr2, arguments='-sP')  #Scanning the network

	file=open(dev_path,'a+')

	for k,v in a['scan'].iteritems(): 
	    if str(v['status']['state']) == 'up':
	        try:
        		if 'Tp-link Technologies' in str(v['vendor']):
        			details = str(v['addresses']['ipv4']) + ' ' + str(v['vendor']) + '\n'
        			for line in file.readlines():
        				if details in line: 
        					inFile = True
        					print 'Already Plug added'
        					break
        			if not inFile:
        				file.write('%d %s' % (id, details))    
        		print str(v['addresses']['ipv4']) + ' => ' + str(v['vendor'])
        	except: print str(v['addresses']['ipv4']) + ' => ' + str(v['vendor'])

	file.close()
	findAddedPlugs()	

def findAddedPlugs(): #This function will read the devices.txt file and will add all the ip addresses 
	wifi_file = open(dev_path, 'r')            #according to their IDs
	#global ips
	for line in wifi_file.readlines():
		if line == '\n':
			wifi_file.close()
			return
		try:
			info = line.split(' ')
			ips.insert(int(info[0])-1, info[1])
			print 'Connected Devices: '
			print 'Id : %s, IP : %s' % (info[0], info[1])
		except Exception as e:
			print 'haa'

	wifi_file.close()


# plug = SmartPlug("192.168.1.53")
# print("Current state: %s" % plug.state)
# #plug.turn_off()
# plug.state = "OFF"
# print("Current state: %s" % plug.state)

client = mqtt.Client()
client.connect(host)

client.on_message = on_message
client.on_connect = on_connect

findAddedPlugs()
client.loop_start()
while (True):
        if(not msgQ.empty()):
                command(msgQ.get())