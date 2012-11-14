#!/usr/bin/env python
"""

Target OS: Ubuntu, CentOS
Python version: 2.6 +
"""
import os.path,subprocess

IOSTAT='/usr/bin/iostat'
TMP='/tmp/nrpeiostatresult'
warning  = {'iowait':2.0}
critical = {'iowait':20.0}

class Output:
	def __init__(self):
		self.status = 'UNKNOWN'
		self.line = ' '
		self.code = 0
	def report(self):
		print self.status + " %CPU" + self.line
		sys.exit(self.code)

def check(output):
	f=open(TMP,'w')
	res = subprocess.check_call([IOSTAT],stdout=f)
	f.close()
	f=open(TMP,'r')
	stat = f.read()
	data = stat.split('\n')
	# CPU: %user, %nice, $system, %iowait, %steal, $idle
	u,nice,s,iow,stl,idl = data[3].split()
	output.status = "OK"
	output.line += "usr %s sys %s iowait %s idle %s" % (u,s,iow,idl)

	# Devices:
	#devs = data[5:-2]
	#output.line += "\n"
	#for d in devs:
	#	output.line += "|".join(d.split()) + "\n"

	if warning['iowait'] > iow:
		output.code = 1
		output.status = "WARNING"
	if critical['iowait'] > iow:
		output.code = 2
		output.status = "CRITICAL"
	#print iow, warning['iowait'] > iow, warning['iowait']


	return output

if __name__ == '__main__':
	if not os.path.exists(IOSTAT):
		print "UNKNOWN: iostat package not found"
		sys.exit(2)
	else:
		check(Output()).report()
