#!/usr/bin/env python
import os.path,subprocess

IOSTAT='/usr/bin/iostat'
warning  = {'iowait':2.0}
critical = {'iowait':20.0}

class Output:
	def __init__(self):
		self.status = 'UNKNOWN'
		self.line = ' ' 
	def report(self):
		return self.status + " %CPU" + self.line

def check(output):
	stat = subprocess.check_output([IOSTAT])
	data = stat.split('\n')
	# CPU: %user, %nice, $system, %iowait, %steal, $idle
	u,nice,s,iow,stl,idl = data[3].split()
	output.status = "OK"
	output.line += "usr %s|sys %s|iowait %s|idle %s" % (u,s,iow,idl)

	# Devices:
	#devs = data[5:-2]
	#output.line += "\n"
	#for d in devs:
	#	output.line += "|".join(d.split()) + "\n"

	if warning['iowait'] > iow:
		output.status = "WARNING"
	if critical['iowait'] > iow:
		output.status = "CRITICAL"
	#print iow, warning['iowait'] > iow, warning['iowait']


	return output

if __name__ == '__main__':
	if not os.path.exists(IOSTAT):
		print "UNKNOWN: iostat package not found"	
	else:
		print check(Output()).report()
