#!/bin/bash
# Rsync to BASEDIR
BASEDIR=/tank/sysadmin/etc
RSYNC=/usr/bin/rsync

rsync -av --progress /etc/pve $BASEDIR &>> /tank/sysadmin/pve-backup.log
