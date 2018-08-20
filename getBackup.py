# Author:	https://github.com/Twigman
# Date:		19.08.2018
# Python 	3.6.5
#
# Description: 
# -----------------------------------------------------------------------------
# Script to get the backup file from an linux system (e.g. raspberry) per SCP.
# Please customize the variables in the 'EDIT REGION' first.
#
# Remember to install the required packages first with 'pip install <package>'.

import logging
import pendulum
import paramiko
from scp import SCPClient, SCPException

def createSSHClient(server, port, user, password):
	client = paramiko.SSHClient()
	client.load_system_host_keys()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(server, port, user, password)
	
	return client
	
def getDateTime():
	return pendulum.now().format('DD-MM-YYYY HH:mm:ss')

# set logger
logging.basicConfig(filename='app.log', level=logging.INFO)

# get date from last Sunday
curDate = pendulum.now()
# sunday = 0, saturday = 6
lastSunday = curDate.subtract(days=curDate.day_of_week)

# ===================
# EDIT REGION - START
# ===================
filename = 'raspberry3Backup' + lastSunday.format('YYYYMMDD') + '.tar.gz'
# source folder of the backup file
source = '/'
# extern HDD
target = 'M:\\'
# your Target IP
targetIP = '192.168.0.1'
# port
targetPort = 22
# target user
username = 'pi'
# his password
pw = ''
# ===================
# EDIT REGION - END
# ===================

try:
	logging.info('[' + getDateTime() + '] started')
	print('Connecting to ' + targetIP + ' as ' + username + ' ...')
	ssh = createSSHClient(targetIP, targetPort, username, pw)
	print('>> [ OK ] Connection established')
	scp = SCPClient(ssh.get_transport())
	print('>> [ OK ] SCP established')
	print('>> Copying ' + filename + ' to ' + target + ' ...')

	try:
		# get the backup file
		scp.get(source + filename, target)
		print('>> [ OK ] File successfully copied')
		logging.info('[' + getDateTime() + '] file copied')
	except SCPException as scpErr:
		print('>> [ FAIL ] ' + str(scpErr))
		logging.error('[' + getDateTime() + '] scp error')
	except FileNotFoundError:
		print('[ FAIL ]' + ' Lokation "' + target + '" is not available')
		print('Hard disk not mounted?')
		logging.error('[' + getDateTime() + '] hdd not mounted')

	scp.close()
	print('>> Connection closed')
except paramiko.ssh_exception.NoValidConnectionsError as connErr:
	print('>> [ FAIL ] ' + str(connErr))
	logging.error('[' + getDateTime() + '] no valid connection')
except TimeoutError as timeout:
	logging.error('[' + getDateTime() + '] timeout')
	print('>> [ FAIL ] ' + str(timeout))
