#!/usr/bin/env python
import sys
import string
import json
import ConfigParser, getopt
from time import sleep
from patlib_old import convertChmodToBinary
from tests import Tester
#begin common part#
def usage():
	print """\033[1m\033[91mCheck file permissions\033[0m\033[0m
	Usage: %s <input> <output>""" % __file__[__file__.rfind('/')+1:]
if __name__ == '__main__':
	try:
		opts, args = getopt.getopt(sys.argv[1:], "i:o", ["init=","output=","help"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for o, a in opts:
		if o in  ("-o","--output"):
			output_folder = a+".log"
		elif o in  ("-i","--init"):
			config_file = a
		else:
			assert False, "unhandled option"
	config = config_file
	#Parser for inputfile
	parser =  ConfigParser.RawConfigParser(allow_no_value=True)
	with open(config, 'r') as g:
		parser.readfp(g)
	#end common part
	#begin parsing input and testing	
	try:
		host			=	parser.get("0","host")
		port 			=	int(parser.get("0","port")) or 22
		if parser.has_option("0","ssh_key_path"):
			ssh_key_path	=	parser.get("0","ssh_key_path")
		else:
			ssh_key_path	=	"~/.ssh/id_rsa"
		ssh_server_key_path	 =	parser.get("0","ssh_server_key_path")
		filepath		=	parser.get("1","filepath")
		chmod			=	parser.get("1","chmod")
		chmod_owner, chmod_group, chmod_other = convertChmodToBinary(chmod)
		username_owner	=	parser.get("2","username_owner")
		tester = Tester(host,username_owner,ssh_key_path,ssh_server_key_path,filepath,chmod,port) 
		#begin testing flow
    step11_status = False
		step12_status = False
		step13_status = False
		step1_status = False
		#[CHECKING CHMOD]
		if tester.checkChmod() == True:
			step11_status = True
		else:
			print "False"
			sys.exit(1)
		#[TESTING OWNER READ]
		if tester.checkRead((chmod_owner)[0]) == True:
			step12_status = True
		#[TESTING OWNER WRITE]
		if tester.checkWrite((chmod_owner)[1]) == True:
			step13_status = True
		if step11_status and step12_status and step13_status:
			step1_status = True
    username_group	=	parser.get("3","username_group")
		tester = Tester(host,username_group,ssh_key_path,ssh_server_key_path,filepath,chmod,port)
		step21_status = False
		step22_status = False
		step2_status = False
		#[TESTING GROUP READ]
		sleep(1)
		if tester.checkRead((chmod_group)[0]) == True:
			step21_status = True
		#[TESTING GROUP WRITE]
		sleep(1)
		if tester.checkWrite((chmod_group)[1]) == True:
			step22_status = True
		if step21_status and step22_status:
			step2_status = True
		username_other	=	parser.get("4","username_other")
		tester = Tester(host,username_other,ssh_key_path,ssh_server_key_path,filepath,chmod,port) 
		#[TESTING OTHER READ]"
		step31_status = False
		step32_status = False
		step3_status = False
		sleep(1)
		if tester.checkRead((chmod_other)[0]) == True:
			step31_status  = True
		#[TESTING OTHER WRITE]
		sleep(1)
		if tester.checkWrite((chmod_other)[1]) == True:
			step32_status = True
		if step31_status and step32_status:
			step3_status = True
		if step1_status and step2_status and step3_status:
			print "True"
		else:
			print "False"
	except:
		raise
		print "False"
	
	