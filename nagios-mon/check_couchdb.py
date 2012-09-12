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
Usage: check_couchdb.py -H <host> [-p <port>] [-w <warn_time>]

  Options:
   -h, --help
      Print detailed help screen
   -H, --hostname=ADDRESS
      Host name, IP Address, or unix socket (must be an absolute path)
   -p, --port=INTEGER
      Port number (default: 389)
   -a [--active]
      Check active worker count instead of job age
beanstalkc 0.3.0 (http://pypi.python.org/pypi/beanstalkc/0.3.0)
        pip install beanstalkc pyyaml
"""

import platform, sys, os
from optparse import OptionParser

try:
    import couchdbkit
except Exception:
    print "Make sure Python has "

