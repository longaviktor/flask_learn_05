import socket
import sys
import time
import os
import paramiko 

from config import systems,local_net


def wol_func(mac,ipr):
	data=''.join(['FF'*6,mac.replace(':','')*16])
	sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	sock.sendto(data.decode("hex"), (ipr,9))

def ping_func(ip):
	response = os.system("ping -c 1 -w1 " + ip)
	if response == 0:
	  return 'Online'
	else:
	  return 'Offline'

def test_ssh_func_key(key,user,ip):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=user, key_filename=key,timeout=1)
        ssh.close()
        return "Online"
    except Exception:
        return "Offline"

def ssh_poweroff_func_key(key,user,ip):
	os.system("ssh -i {0} {1}@{2} sudo poweroff".format(key,user,ip))

def ssh_reboot_func_key(key,user,ip):
	os.system("ssh -i {0} {1}@{2} sudo reboot".format(key,user,ip))




class wol:
	def wol_1(self):
		wol_func(systems().mac1(),local_net().ipr())

class ping:
	def ping_1(self):
		return ping_func(systems().ip1())

class poweroff:
	def poweroff_1(self):
		ssh_poweroff_func_key(systems().key1(),systems().user1(),systems().ip1())

class reboot:
	def reboot_1(self):
		ssh_reboot_func_key(systems().key1(),systems().user1(),systems().ip1())

class testssh:
	def testssh_1(self):
		return test_ssh_func_key(systems().key1(),systems().user1(),systems().ip1())

class local:
	def poweroff(self):
		os.system("sudo poweroff")
	def reboot(self):
		os.system("sudo reboot")
	def reapache(self):
		os.system("sudo /etc/init.d/apache2 restart")





