#!/usr/bin/python3
# ver 1.0

import paho.mqtt.client as mqtt
import json
import os
import time
#import threading
from parameter.parameter import *
#from queue import Queue
from datetime import datetime
from colorama import Fore, Back, Style

import syslog_client  #  from local folder !

mqttclient_log=False
#q=Queue()

COLOR_TOGGLE = True
NR = 0

'''
print(Fore.RED + 'some red text')
print(Back.GREEN + 'and with a green background')
print(Style.DIM + 'and in dim text')
print(Style.RESET_ALL)
print('back to normal now')
'''

class MQTTClient(mqtt.Client):#extend the paho client class
   run_flag=False #global flag used in multi loop
   def __init__(self,cname,**kwargs):
      super(MQTTClient, self).__init__(cname,**kwargs)
      self.last_pub_time=time.time()
      self.topic_ack=[] #used to track subscribed topics
      self.run_flag=True
      self.submitted_flag=False #used for connections
      self.subscribe_flag=False
      self.bad_connection_flag=False
      self.bad_count=0
      self.connected_flag=False
      self.connect_flag=False #used in multi loop
      self.disconnect_flag=False
      self.disconnect_time=0.0
      self.pub_msg_count=0
      self.pub_flag=False
      self.sub_topic=""
      self.sub_topics=[] #multiple topics
      self.sub_qos=0
      self.devices=[]
      self.broker=""
      self.port=1883
      self.keepalive=60
      self.run_forever=False
      self.cname=""
      self.delay=10 #retry interval
      self.retry_time=time.time()

def Initialise_clients(cname,mqttclient_log=False,cleansession=True,flags=""):
   client= MQTTClient(cname,clean_session=cleansession)
   client.cname=cname
   client.on_connect= on_connect        #attach function to callback
   client.on_message=on_message        #attach function to callback

   return client

def on_connect(client, userdata, flags, rc):
   """
   set the bad connection flag for rc >0, Sets onnected_flag if connected ok
   also subscribes to topics
   """
   
   if rc==0:
      client.connected_flag=True #old clients use this
      client.bad_connection_flag=False
      if client.sub_topic!="": #single topic
         print("subscribing "+str(client.sub_topic))
         print("subscribing in on_connect")
         topic=client.sub_topic
         if client.sub_qos!=0:
            qos=client.sub_qos
         client.subscribe(topic,qos)
      elif client.sub_topics!="":
         #print("subscribing in on_connect multiple")
         client.subscribe(client.sub_topics)

   else:
     print("set bad connection flag")
     client.bad_connection_flag=True 
     client.bad_count +=1
     client.connected_flag=False 

def on_message(client,userdata, msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    message_handler(client,m_decode,topic)
    #print("message received")

def message_handler(client,msg,topic):
    data=dict()
    now = datetime.now()
    epoch=time.time()
    tnow=now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # with miliseconds
    #m=time.asctime(tnow)+" "+topic+" "+msg
    try:
        msg=json.loads(msg)#convert to Javascript before saving
        #print("json data")
    except:
        pass
        #print("not already json")
    
    data["topic"]=topic
    data["message"]=msg
    data["epoch"]=epoch
    data["time"]=tnow
    do_log(data)

def has_changed(client,topic,msg):
    topic2=topic.lower()
    if topic2.find("control")!=-1:
        return False
    if topic in client.last_message:
        if client.last_message[topic]==msg:
            return False
    client.last_message[topic]=msg
    return True

def do_log(msg):
    global COLOR_TOGGLE,NR,log
    if options["do_syslog"]:
        log.send(msg, 25)
    if options["do_screen_full"]:
        #print(json.dumps(results,indent=2))
        print(msg)
    if options["do_screen_short"]:
        #print(json.dumps(results,indent=2))
        timestamp = datetime.fromtimestamp( msg["epoch"] )  
        line=timestamp.strftime( "%H:%M:%S.%f")[:-3]
        line += " " + msg["topic"] + " - "
        if COLOR_TOGGLE:
            c=Fore.CYAN
        else:
            c=Fore.GREEN
        print(c+str(NR),line, msg["message"])
        COLOR_TOGGLE = not COLOR_TOGGLE
        NR += 1


            
#--------------  MAIN  --------------

if options["do_syslog"]:   
    log = syslog_client.Syslog(host=options["sys_address"])

cname = options["cname"]

client=Initialise_clients(cname,mqttclient_log,False)  #create and initialise client object

client.username_pw_set(options["broker"]["username"], options["broker"]["password"])
client.sub_topics=options["topics"]
client.broker=options["broker"]["ip"]
client.port=options["broker"]["port"]
client.last_message=dict()


try:
    res=client.connect(client.broker,client.port)      #connect to broker
    client.loop_start() #start loop

except:
    print("connection to ",client.broker," failed")
    raise SystemExit("connection failed")
try:
    while True:
        time.sleep(1)
        pass

except KeyboardInterrupt:
    print("interrrupted by keyboard")

client.loop_stop() #start loop
#Log_worker_flag=False #stop logging thread
#time.sleep(5)
time.sleep(1)
