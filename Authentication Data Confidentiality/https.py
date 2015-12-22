#!/usr/bin/python
from xml.dom.minidom import parseString
import logging
import subprocess
import ConfigParser
import time
import datetime, dateutil.parser
import pdb

def httpsParser(xml_message):
	status=False;
	#output_toparse="/Users/iridium/Jobs/testManager/testManager/XMLRepository/nmap.txt"
	#with open(output_toparse,'r') as f:
					#result=result+ev_code+"$"+f.read()+"\n"
	#				xml_message=f.read()
	now=time.time()




	dom = parseString(xml_message)
	host=dom.getElementsByTagName("nmaprun")[0].getElementsByTagName("host")[0]
	#print "HOSTNAME: "+host.getElementsByTagName("hostname")[0].getAttribute("name")

	port=host.getElementsByTagName("ports")[0].getElementsByTagName("port")[0]
	#print "PORT: "+port.getAttribute("portid")

	if port.getElementsByTagName("state")[0].getAttribute("state")!="open":
		return False
	'''if port.getElementsByTagName("service")[0].getAttribute("name") !="https":
		return False
	'''
	#print "PORT STATE: "+port.getElementsByTagName("state")[0].getAttribute("state")
	#print "SERVICE RUNNING: "+port.getElementsByTagName("service")[0].getAttribute("name")
	ssl_scripts=port.getElementsByTagName("script")
	for script in ssl_scripts:
		if script.getAttribute("id")=="ssl-cert":
			ssl_cert=script
		if script.getAttribute("id")=="ssl-enum-ciphers":
			ssl_cipher=script

	table=ssl_cert.getElementsByTagName("table")
	for info in table:
		if info.getAttribute("key")=="validity":
			values=info.getElementsByTagName("elem")
			for value in values:
				if value.getAttribute("key")=="notBefore":
					notBefore = dateutil.parser.parse(value.childNodes[0].nodeValue)
					notBefore = int(notBefore.strftime("%s"))
					if notBefore>now :
						return False

					#print "NOT VALID BEFORE: "+value.childNodes[0].nodeValue
				if value.getAttribute("key")=="notAfter":
					notAfter= dateutil.parser.parse(value.childNodes[0].nodeValue)
					notAfter = int(notAfter.strftime("%s"))
					if notAfter<now :
						return False
						#sys.exit()
					#print "NOT VALID AFTER: "+value.childNodes[0].nodeValue


	table=ssl_cipher.getElementsByTagName("elem")
	for info in table:

		if info.getAttribute("key")=="least strength":
			if info.childNodes[0].nodeValue=="weak":
				return False


			#print "KEY STRENGTH:"+info.childNodes[0].nodeValue
	return True

#output_toparse="/Users/iridium/result.xml"
#with open(output_toparse,'r') as f:
					#result=result+ev_code+"$"+f.read()+"\n"
#	xml_message=f.read()
#print xml_message
#print httpsParser(xml_message)
