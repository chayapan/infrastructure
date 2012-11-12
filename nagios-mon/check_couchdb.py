#!/usr/bin/env python
# Copyright 2012, Chayapan Khannabha <chayapan@gmail.com>.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

"""check_couchdb.py  monitors CouchDB with Nagios and NRPE
Usage: check_couchdb.py -H <host> [-p <port>] [-w <warn_time>] [-U <user:pwd>]

  Options:
   -h, --help
      Print detailed help screen
   -U, --user
      User account to connect. username:password
   -H, --hostname=ADDRESS
      Host name, IP Address, or unix socket (must be an absolute path)
   -p, --port=INTEGER
      Port number (default: 5984)
   -a [--active]
      Check active worker count instead of job age
couchdb (http://pypi.python.org/pypi/couchdb)
        pip install couchdb
"""

import platform, sys, os
from optparse import OptionParser

try:
    import couchdb
except Exception:
    print """SERVICE STATUS: Missing dependency. Make sure Python has couchdb. Try 'pip install couchdb'"""
    sys.exit(3)

def couchdb_up(hostname,account=False):
    #try:
    server = couchdb.Server(host)

def couchdb_stats():
	print "stats"

def main():
	parser = OptionParser() # __doc__
	parser.add_option('-H', '--hostname',	dest="host",
		default='localhost', help="Couchdb hostname")
	parser.add_option('-p', '--port',	dest="port",
		default='5984', help="Couchdb port")
	parser.add_option('-v', '--verbose',	dest="verbose",
		default='0', help="Output details, 0-3")
	parser.add_option('-c',dest="threshold_critical")
	parser.add_option('-w',dest="threshold_warning")
	parser.add_option('-U','--user',	dest="user",
		default='', help="User account")

	(options, args) = parser.parse_args()
		
	host = "http://%(user)s%(host)s:%(port)s" % { 
		'user' : options.user,
		'host' : options.host,
		'port' : options.port
	}
	service_status = couchdb_up(host)
	if (int(options.verbose) > 0 and service_status == 0):
		couchdb_stats(host,port)
	return service_status

if (__name__=='__main__'):
    sys.exit(main())
