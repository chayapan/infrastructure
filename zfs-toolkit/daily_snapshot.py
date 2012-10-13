#!/usr/bin/env python
import os,subprocess,datetime,logging
logging.basicConfig(	filename='/tmp/snapshot.log',
			level=logging.INFO,
			format='%(asctime)s %(message)s')
ZFS = '/sbin/zfs'
ZPOOL = '/sbin/zpool'
snaptime = datetime.datetime.now().strftime('%Y%m%d.h%H')

err=open("/tmp/snapshot.err","w")
err.write(snaptime)


def create_hourly_snapshot():
	print snaptime
	fs = "tank/vm"
	cmd = "%(zfs)s snap %(tgt)s@%(ts)s" % {'zfs':ZFS, 'tgt':fs, 'ts':snaptime }
	print cmd
	subprocess.call(cmd.split(" "),stderr=err)

def rotate_snapshots(i=4,tgt="tank/vmbak"):
  """ Assume there are i+1 snapshots to be kept
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
  cmd = "%(zfs)s snap %(tgt)s@last.0" % {'zfs': ZFS, 'tgt': tgt}
  cmd_list.append(cmd)
  
  #print cmd_list
  for cmd in cmd_list:
    logging.info(cmd)
    subprocess.call(cmd.split(" "),stderr=err)

if __name__ == '__main__':
  rotate_snapshots(tgt="tank/vm")
  rotate_snapshots(tgt="tank/vmbak")

err.close()
