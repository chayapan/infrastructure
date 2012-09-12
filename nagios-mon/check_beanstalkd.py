#!/usr/bin/env python
# Copyright 2012, Chayapan Khannabha <chayapan@gmail.com>.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

"""check_beanstalkd.py	monitors Beanstalkd with Nagios and NRPE
Usage: check_beanstalkd.py -H <host> [-p <port>] [-t <tube>] [-w <warn_time>] [-c <crit_time>]

  Options:
   -h, --help
      Print detailed help screen
   -H, --hostname=ADDRESS
      Host name, IP Address, or unix socket (must be an absolute path)
   -p, --port=INTEGER
      Port number (default: 389)
   -a [--active]
      Check active worker count instead of job age
   -t [--tube]
      Tube name to watch, can be multiple. 
   -w, --warning=DOUBLE
      Response time to result in warning status (seconds), or min worker count
   -c, --critical=DOUBLE
      Response time to result in critical status (seconds), or min worker count
   -v, --verbose
      Show details for command-line debugging (Nagios may truncate output)

Examples:
	./check_beanstalkd -H 127.0.0.1 -p 11300

put some jobs into beanstalk
import string,random
word = lambda : "".join([ random.choice(string.ascii_lowercase) for i in range(rand.int) ])
[ bs.put(word()) for i in range(500) ]

Credits:
  mon api:
	http://search.cpan.org/~gbarr/Nagios-Plugin-Beanstalk-0.04/lib/Nagios/Plugin/Beanstalk.pm
  python cmd line program pattern:
	https://github.com/openstack/swift/blob/master/bin/swift-init	

beanstalkc 0.3.0 (http://pypi.python.org/pypi/beanstalkc/0.3.0)
	pip install beanstalkc pyyaml
"""

import platform, sys, os
from optparse import OptionParser

try:
	import beanstalkc
except Exception:
	print "Make sure Python has beanstalkc, pyyaml. Check pip freeze"
	sys.exit(1)

def beanstalkd_up(hostname,port):
	bs = beanstalkc.Connection(host=hostname,port=port)
	return "OK, Beanstalk is UP";

def beanstalkd_stats(hostname,port):
	bs = beanstalkc.Connection(host=hostname,port=port)
	stat = bs.stats()
	report = """Uptime:%(uptime)10d; Total jobs:%(total_jobs)7d; Tubes:%(tubes)3d"""	
	return report % {'uptime': stat['uptime'],
			 'total_jobs': stat['total-jobs'],
			 'tubes': stat['current-tubes']
			 }

def main():
	parser = OptionParser() # __doc__
	parser.add_option('-H', '--hostname',	dest="host",
		help="Beanstalkd hostname")
	parser.add_option('-p', '--port',	dest="port")
	parser.add_option('-c',dest="threshold_critical")
	parser.add_option('-w',dest="threshold_warning")

	(options, args) = parser.parse_args()
	#print options
	host = options.host
	port = int(options.port)
	print beanstalkd_up(host,port)
	print beanstalkd_stats(host,port)
	return 0

if __name__=='__main__':
  sys.exit(main())
