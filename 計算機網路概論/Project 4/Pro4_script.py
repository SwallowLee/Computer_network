from mininet.log import setLogLevel, info
from mininet.net import Mininet
from mininet.cli import CLI

from mininet.opennet import Pcap
from mininet import ns3

import ns.wifi

def mobile_ip_topo():
	net = Mininet(controller = None)
	# Add hosts and switches
	h1 = net.addHost( 'h1' ,ip='192.168.1.2/24')
	h2 = net.addHost( 'h2' ,ip='192.168.4.2/24')
	s1 = net.addSwitch( 's1' )
	s2 = net.addSwitch( 's2' )
	router1 = net.addHost( 'router1', ip='192.168.1.1/24' )
	router2 = net.addHost( 'router2', ip='192.168.2.2/24' )
	router3 = net.addHost( 'router3', ip='192.168.3.2/24' )

	# Add links
	net.addLink( h1, s1 )
	net.addLink( h2, s2 )
	net.addLink( s1, router1 )
	net.addLink( router1, router2 )
	net.addLink( router2, router3 )
	net.addLink( s2, router3 )
		
	net.start()
    	ns3.start()
	# Setting switches 
    	s1.cmdPrint( 'ovs-vsctl set-fail-mode s1 standalone' )
    	s2.cmdPrint( 'ovs-vsctl set-fail-mode s2 standalone' )

	# setting router
	router1.cmdPrint( 'ip addr add dev router1-eth1 192.168.2.1/24' )
    	router1.cmdPrint( 'sysctl -w net.ipv4.ip_forward=1' )
	router1.cmdPrint( 'ip route add 192.168.3.0/24 via 192.168.2.2' )
	router1.cmdPrint( 'ip route add 192.168.4.0/24 via 192.168.2.2' )
	router2.cmdPrint( 'ip addr add dev router2-eth1 192.168.3.1/24' )
    	router2.cmdPrint( 'sysctl -w net.ipv4.ip_forward=1' )
	router2.cmdPrint( 'ip route add 192.168.1.0/24 via 192.168.2.1' )
	router2.cmdPrint( 'ip route add 192.168.4.0/24 via 192.168.3.2' )
	router3.cmdPrint( 'ip addr add dev router3-eth1 192.168.4.1/24' )
    	router3.cmdPrint( 'sysctl -w net.ipv4.ip_forward=1' )
	router3.cmdPrint( 'ip route add 192.168.1.0/24 via 192.168.3.1' )
	router3.cmdPrint( 'ip route add 192.168.2.0/24 via 192.168.3.1' )

	# setting host
	h1.cmdPrint( 'ip route add default via 192.168.1.1' )
	h2.cmdPrint( 'ip route add default via 192.168.4.1' )

	CLI( net )

	ns3.stop()
	ns3.clear()
	net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    mobile_ip_topo()
