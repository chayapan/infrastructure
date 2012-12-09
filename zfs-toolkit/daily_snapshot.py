#!/usr/bin/env python
"""
  TODO: 
   - implement hourly snapshot
   - measure performance for this rotating strategy
"""
import os,subprocess,datetime,logging
logging.basicConfig(	filename='/tank/sysadmin/snapshot.log',
			level=logging.INFO,
			format='%(asctime)s %(message)s')
logging.basicConfig(	filename='/tank/sysadmin/snapshot.error',
			level=logging.ERROR,
			format='%(asctime)s %(message)s')
ZFS = '/sbin/zfs'
ZPOOL = '/sbin/zpool'
snaptime = datetime.datetime.now().strftime('%Y%m%d.h%H')
#logging.info("Start snapshot at " + snaptime)

def create_hourly_snapshot():
	print snaptime
	fs = "tank/vm"
	cmd = "%(zfs)s snap %(tgt)s@%(ts)s" % {'zfs':ZFS, 'tgt':fs, 'ts':snaptime }
	print cmd
	subprocess.call(cmd.split(" "),stderr=err)

def rotate_snapshots(i=4,tgt="tank/vmbak"):
  """ Assume there are i+1 snapshots to be kept
     1. destroy oldest snapshot
     2. rename snapshots
     3. create new snapshot 
  """
  #print i, "%(zfs)s destroy %(tgt)s@last.%(last)s" % {'zfs': ZFS, 'tgt': tgt, 'last': i}
  cmd = "%(zfs)s destroy %(tgt)s@last.%(last)s" % {'zfs': ZFS, 'tgt': tgt, 'last': i}
  cmd_list = [cmd]
  for i in [4,3,2,1]:
     #print i, "%(zfs)s rename %(tgt)s@last.%(from)s %(tgt)s@last.%(to)s" % {
     #			'zfs':ZFS, 'tgt':tgt, 'from':i-1, 'to':i }
     cmd = "%(zfs)s rename %(tgt)s@last.%(from)s %(tgt)s@last.%(to)s" % {
			'zfs':ZFS, 'tgt':tgt, 'from':i-1, 'to':i }
     cmd_list.append(cmd)
  cmd = "%(zfs)s snapshot %(tgt)s@last.0" % {'zfs': ZFS, 'tgt': tgt}
  cmd_list.append(cmd)
  
  #print cmd_list
  for cmd in cmd_list:
    logging.info(cmd)
    subprocess.call(cmd.split(" "))

if __name__ == '__main__':
  """
    Assume 4 datasets: tank/vm tank/sysadmin tank/othello tank/dune
  """
  logging.info("Start snapshot at " + snaptime)
  rotate_snapshots(tgt="tank/vm")
  rotate_snapshots(tgt="tank/sysadmin")
  rotate_snapshots(tgt="tank/othello")
  rotate_snapshots(tgt="tank/dune")
  logging.info("End snapshot at " + snaptime)
