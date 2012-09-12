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


def beanstalkc_installed():
	__doc__ = """Make sure Python has beanstalkc, pyyaml
			try: pip install beanstalkc pyyaml"""
	try:
		import beanstalkc
	catch Exception:
		print __doc__

def beanstalkd_up():
	print "OK Beanstalk is UP";


def main():
	parser = OptionParser() # __doc__
	parser.add_option('-H', '--hostname',	dest="hostaddress",
		help="Beanstalkd hostname")
	parser.add_option('-p', '--port',	dest="port")
	parser.add_option('-c',dest="threshold_critical")
	parser.add_option('-w',dest="threshold_warning")

	(options, args) = parser.parse_args()
	#print options
	beanstalkc_installed()
	beanstalkd_up()

if __name__=='__main__':
  sys.exit(main())
