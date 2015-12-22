#!/usr/bin/env python
import sys
import string
import ConfigParser, getopt
import time
import dateutil
import subprocess
from https import httpsParser

#begin common part#
def usage():
	print """\033[1m\033[91mCheck SSL/TSL\033[0m\033[0m
	Usage: %s <input> <output>""" % __file__[__file__.rfind('/')+1:]
if __name__ == '__main__':
	try:
		opts, args = getopt.getopt(sys.argv[1:], "i:o:", ["init=","output=","help"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for o, a in opts:
		if o in  ("-o","--output"):
			output = a
		elif o in  ("-i","--init"):
			config_file = a
		else:
			assert False, "unhandled option"
	config = config_file
	#Parser for inputfile

	try:
		parser =  ConfigParser.RawConfigParser(allow_no_value=True)
		with open(config, 'r') as g:
			parser.readfp(g)
	#end common part
	#begin parsing input and testing

		host=parser.get("0","host")
		if parser.has_option("0","port"):
			port=parser.get("0","port")
		else:
			port=443

		pathexecutor = "nmap -oX "+output+" --script ssl-cert,ssl-enum-ciphers -p "+port+" "+host+">"+output+".log"
		proc = subprocess.Popen([pathexecutor], stdout=subprocess.PIPE, shell=True)
		(out, err) = proc.communicate()

		with open(output,'r') as f:
			xml_result=f.read()
			result=httpsParser(xml_result);
			print result
	except:
		raise
		print "False"
