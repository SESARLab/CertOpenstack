__author__ = 'Patrizio Tufarolo'
__email__ = 'patrizio.tufarolo@studenti.unimi.it'

from neutronclient.v2_0 import client as NeutronClient
from novaclient.client import Client as NovaClient
from keystoneclient.auth.identity import v2 as KeystoneClient
from keystoneclient import session as KeystoneSession



import pdb

'''old probe format compatibility layer'''
import ConfigParser, getopt, sys
def usage():
	print """\033[1m\033[91mParses a security group with a given ID\033[0m\033[0m
	Usage: %s -i <input>""" %__file__[__file__.rfind('/')+1:]
def exit_from_test():
	sys.exit(1)

try:
	opts, args = getopt.getopt(sys.argv[1:], "h:i:", ["help=","input="])
except getopt.GetoptError:
	usage()
	sys.exit(2)
config_file = None
for o, a in opts:
	if o in ["-h","--help"]:
		usage()
	elif o in ["-i","--input"]:
		config_file = a

if config_file is None:
	usage()
	sys.exit(2)
parser = ConfigParser.RawConfigParser(allow_no_value=True)
try:
	with open(config_file,'r') as g:
		parser.readfp(g)
except IOError:
	print "No such file or directory"
	sys.exit(2)

'''/old probe template compatibility layer'''


'''testAgentComponents Wrapper'''
from testAgentComponents import TestCase
from testAgentComponents import TestInstance
from testAgentComponents import Probe

tc = TestCase("tc","Neutron - Parse Security Group")


ti0 = TestInstance("0")
ti0.appendInput("MIN_PORT",parser.get("0","MIN_PORT"))
ti0.appendInput("MAX_PORT",parser.get("0","MAX_PORT"))
ti0.appendInput("TARGET_IP",parser.get("0","TARGET_IP"))
ti0.appendInput("TARGET_UUID",parser.get("0","TARGET_UUID"))
tc.appendTestInstance(ti0)


ti1 = TestInstance("1")
ti1.appendInput("OS_AUTH_URL",parser.get("1","OS_AUTH_URL"))
ti1.appendInput("OS_TENANT_NAME",parser.get("1","OS_TENANT_NAME"))
ti1.appendInput("OS_TENANT_ID",parser.get("1","OS_TENANT_ID"))
ti1.appendInput("OS_USERNAME",parser.get("1","OS_USERNAME"))
ti1.appendInput("OS_PASSWORD",parser.get("1","OS_PASSWORD"))
ti1.appendInput("OS_REGION_NAME",parser.get("1","OS_REGION_NAME"))
tc.appendTestInstance(ti1)
ti2 = TestInstance("2")
ti2.appendInput("ENABLE_TCP_SCAN",parser.get("2","ENABLE_TCP_SCAN"))
ti2.appendInput("ENABLE_UDP_SCAN",parser.get("2","ENABLE_UDP_SCAN"))
ti2.appendInput("TCP_SYN_SCAN",parser.get("2","TCP_SYN_SCAN"))
tc.appendTestInstance(ti2)



'''/testAgentComponents Wrapper'''


def nullRollback(inputData,testInstances):
	return

def createNeutronClient(inputData,testInstances):
	neucl = NeutronClient.Client(auth_url=testInstances["1"]["OS_AUTH_URL"],
					username=testInstances["1"]["OS_USERNAME"],
					password=testInstances["1"]["OS_PASSWORD"],
					tenant_name=testInstances["1"]["OS_TENANT_NAME"],
					region_name=testInstances["1"]["OS_REGION_NAME"])
	keystonecl = KeystoneClient.Password(auth_url=testInstances["1"]["OS_AUTH_URL"],
					username=testInstances["1"]["OS_USERNAME"],
					password=testInstances["1"]["OS_PASSWORD"],
					tenant_name=testInstances["1"]["OS_TENANT_NAME"])
	sess = KeystoneSession.Session(auth=keystonecl)
	novacl = NovaClient(3,session=sess)

	return neucl,novacl



def parseSecurityGroup(inputData,testInstances):
	neucl,novacl = inputData
	allSecurityGroups = novacl.servers.get(testInstances["0"]["TARGET_UUID"]).list_security_group()
	allSecurityGroups_details = []
	for sg in allSecurityGroups:
		allSecurityGroups_details.append(neucl.show_security_group(str(sg)))

	dict_tcp = {}
	dict_udp = {}
	list_tcp = []
	list_udp = []
	icmp = 0
	for sg in allSecurityGroups_details:
		for rule in sg['security_group']['security_group_rules']:
			if rule["direction"] == "ingress":
				if rule["protocol"] == "icmp":
					icmp = 1 if icmp == 0 else icmp
				
				elif rule["port_range_min"] and rule["port_range_max"]:
					for i in range(rule["port_range_min"],rule["port_range_max"]+1):
						if i >= int(testInstances["0"]["MIN_PORT"]) and i <= int(testInstances["0"]["MAX_PORT"]):
							if rule["protocol"] == "tcp":
								dict_tcp[i] = 1
							if rule["protocol"] == "udp":
								dict_udp[i] = 1

	for k,v in dict_tcp.iteritems():
		if v == 1:
			list_tcp.append(k)

	for k,v in dict_udp.iteritems():
		if v == 1:
			list_udp.append(k)

	return icmp, list_tcp, list_udp







############################################################
################    	  NMAP PART 		################
################ 	added on 02/22/2015		################
############################################################

from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException

def doRealScan(inputData,testInstances):
	icmp_flag, list_tcp, list_udp = inputData
	def do_scan(targets,options):
		parsed = None
		proc = NmapProcess(targets,options)
		running = proc.run()
		if running != 0:
			raise Exception("Scan failed")
		return NmapParser.parse(proc.stdout)
	options = ""
	options = options + " -Pn -p"+testInstances["0"]["MIN_PORT"]+"-"+testInstances["0"]["MAX_PORT"]+" -s"
	if testInstances["2"]["ENABLE_TCP_SCAN"] == "1":
		options = options + "S" if testInstances["2"]["TCP_SYN_SCAN"] == "True" else options + "T"
	if testInstances["2"]["ENABLE_UDP_SCAN"] == "1":
		options = options + "U"
	scanResults = do_scan(testInstances["0"]["TARGET_IP"],options)
	for host in scanResults.hosts:
		for port, protocol in host.get_open_ports():
			if protocol == "tcp" and port not in list_tcp:
				return False
			if protocol == "udp" and port not in list_udp:
				return False
	return True 



probe = Probe()
probe.appendAtomic(createNeutronClient,nullRollback)
probe.appendAtomic(parseSecurityGroup,nullRollback)
probe.appendAtomic(doRealScan,nullRollback)
result  = probe.run(tc)
r1, r2 = result
print r1 and r2