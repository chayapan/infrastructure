#!/usr/bin/env python
"""Nagios plugin for CPU time monitoring. Focusing on %iowait.
OS: Ubuntu, CentOS (requires sysstat package)
Python version: 2.6 +
"""
import sys,os.path,subprocess

IOSTAT='/usr/bin/iostat'
TMP='/tmp/nrpeiostatresult'
# Device we're interested in
DEV=['sda','sdb','sdc','sdd','vda','vbd','vdc','vdd']

warning  = {'iowait':2.0}
critical = {'iowait':20.0}

class Output:
    code = {'UNKNOWN':2, 'CRITICAL':2, 'WARNING':1, 'OK':0}
    def __init__(self):
        self.status = 'UNKNOWN'
        self.line = ' '
    def __repr__(self):
        return self.status + " %CPU" + self.line

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
    devs = data[5:-2]
    output.line += " "+",".join(devs[0].split())  # column headers
    for line in devs:
	dev = line.split()
        if dev[0] in DEV:
            output.line += " " + ",".join(line.split()) # device row

    if warning['iowait'] > iow:
        output.code = 1
        output.status = "WARNING"
    if critical['iowait'] > iow:
        output.code = 2
        output.status = "CRITICAL"
    #print iow, warning['iowait'] > iow, warning['iowait']
    return output

if __name__ == '__main__':
    status = Output()
    if not os.path.exists(IOSTAT):
        status.status = 'UNKNOWN'
        status.line = " iostat not found (install sysstat package)"
    else:
        status = check(status)
    print status
    sys.exit(status.code[status.status])
