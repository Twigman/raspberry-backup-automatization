#!/bin/bash
# Creates a full backup as 'root' in the root folder (/) and changes
# the owner to 'pi'.
# 1. Copyt the file to /root/
# 2. Create a cronjob with 'crontab -e' and set the schedule to: 
# 0 5 * * 0		/root/backup.sh
# This will execute the script every sunday at 5 am.

now=$(date +"%Y%m%d")
name="raspberry3Backup$now.tar.gz"

cd /
tar -cvpzf $name --exclude=/$name --one-file-system / 
chown pi /$name
