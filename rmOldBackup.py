#!/usr/bin/python2.7
# Author:	https://github.com/Twigman
# Date:		19.08.2018
# Clean up script.
# Removes the old backup file (last sunday) and keeps only the new one.
# Should be executed on Sunday after the new backup.
# 0 8 * * 0		python2.7 /root/rmOldBackup.py
# For the gmailtwigman module look at https://github.com/Twigman/python-send-gmail

import pendulum
import os
from gmailtwigman import sender

backupFolder = '/'

now = pendulum.now()
oldDate = now.subtract(days=7)
oldBackupFile = 'raspberry3Backup' + oldDate.format('YYYYMMDD') + '.tar.gz'
newBackupFile = 'raspberry3Backup' + now.format('YYYYMMDD') + '.tar.gz'

# check if new Backup file exists
if os.path.isfile(backupFolder + newBackupFile):
	print('>> New backup exists: ' + backupFolder + newBackupFile)
	# is the old Backup there too?
	if os.path.isfile(backupFolder + oldBackupFile):
		print('>> Old backup exists too: ' + oldBackupFile)
		print('>> Removing old backup ' + backupFolder + oldBackupFile)
		os.remove(backupFolder + oldBackupFile)
		print('>> File removed!')
	else:
		print('>> Old backup already removed (' + backupFolder + oldBackupFile + ')')
else:
	print('>> There is no current backup! Something went wrong!')
	# Send mail
	fromEmail = 'from@example.com'
	toEmail = 'to@example.com'
	subject = 'Backup failure'
	body = 'During the backup cleaning process no current backup was found.\nThe current backupfile should be: ' + backupFolder + newBackupFile
	sender.SendEmail(fromEmail, toEmail, subject, body)	




