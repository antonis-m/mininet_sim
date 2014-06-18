'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment: Layer-2 Firewall Application

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
import csv



log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]  


class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):    
        ''' Add your logic here ... '''
        log.debug("Connection %s " % (event.connection,)) 
        fd=open(policyFile,'r')
	csvreader = csv.reader(fd, delimiter=',')
        next(fd)
        #read send one message per line
	print "START"
     	for line in csvreader: 
          print line

          msg1=of.ofp_flow_mod()
          msg1.priority=150
          msg2=of.ofp_flow_mod()
          msg2.priority=150

          match1=of.ofp_match()
          match1.dl_src=EthAddr(line[1])
          match1.dl_dst=EthAddr(line[2])
         
          match2=of.ofp_match()
          match2.dl_src=EthAddr(line[2])
          match2.dl_dst=EthAddr(line[1])

          msg1.match = match1
          msg1.buffer_id=None
          msg1.idle_timeout=30
          msg1.hard_timeout=60
          
          msg2.match = match2
          msg2.buffer_id=None
          msg2.idle_timeout=30
          msg2.hard_timeout=60
          event.connection.send(msg1)
          event.connection.send(msg2)
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    core.registerNew(Firewall)
