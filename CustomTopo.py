'''
Coursera:
- Software Defined Networking (SDN) course

-- Programming Assignment 2

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta, Muhammad Shahbaz
'''

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from mininet.link import TCLink

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
        # Add your logic here ...
	self.fanout=fanout
        self.linkopts1=linkopts1
        core=self.addSwitch('c1')
        aggregates=[]        
	edge=[]
	hosts=[]
	for i in range(fanout):
		aggregates.append(self.addSwitch('a%s' % str(i+1)))  
                self.addLink(core,aggregates[i],bw=linkopts1['bw'], delay=linkopts1['delay'])                
		for j in range(fanout):
			index=i*fanout + j
			edge.append(self.addSwitch('e%s' % str(index+1)))  
			self.addLink(aggregates[i],edge[index],bw=linkopts2['bw'], delay=linkopts2['delay'])	
			for k in range(fanout):
        			host_index=index*fanout+k
				hosts.append(self.addHost('h%s' % str(host_index+1))) 
				self.addLink(edge[index],hosts[host_index],bw=linkopts3['bw'], delay=linkopts3['delay'])

def simpleTest():
   "Create and test a simple network"
   linkopts1 = {'bw':50, 'delay':'5ms'}
   "--- aggregation to edge switches"
   linkopts2 = {'bw':30, 'delay':'10ms'}
   "--- edge switches to hosts"
   linkopts3 = {'bw':10, 'delay':'15ms'}

   topo = CustomTopo(linkopts1,linkopts2,linkopts3,fanout=3)
   net = Mininet(topo,link=TCLink)
   net.start()
   print "Dumping host connections"
   dumpNodeConnections(net.hosts)
   print "Testing network connectivity"
   net.pingAll()
   net.stop()
            
if __name__ == '__main__':
   # Tell mininet to print useful information
   setLogLevel('info')
   simpleTest()
        
#topos = { 'custom': ( lambda: CustomTopo() ) }
