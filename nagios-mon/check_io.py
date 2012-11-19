#!/usr/bin/env python
"""Nagios plugin for CPU time monitoring
OS: Ubuntu, CentOS
Python version: 2.6 +
Requires sysstat package
"""
import sys,os.path,subprocess

IOSTAT='/usr/bin/iostat'
TMP='/tmp/nrpeiostatresult'
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
    #devs = data[5:-2]
    #output.line += "\n"
    #for d in devs:
    #   output.line += "|".join(d.split()) + "\n"

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
        status.line = "iostat package not found"
    else:
        status = check(status)
    print status
    sys.exit(status.code[status.status])
