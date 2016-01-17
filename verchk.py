#!/usr/bin/python

import sys
import time

import xmltodict

from device import Device

import shlex
import subprocess

import json

file_list = sys.argv

#print "\nfile_list: ",file_list
#print "\nfile_list.count): ",len(file_list)

if len(file_list) == 3:
	print "\nEnough arguments have been passed"
else:
	print '\nNot enough arguments, please re-enter with "approved version" and " IP address"'
	exit()

app_file_name = file_list[1]
ip_file_name = file_list[2]

file_object = open(app_file_name,"r")
app_version = file_object.readline().strip()
print "\nThis is the approved version: ",app_version,"\n\tSwitches not running this version will require an upgrade"

ip_file_object = open(ip_file_name,"r")
ip_addresses = ip_file_object.readline().strip()
ip_address_list = ip_addresses.split(',')

for each_ip in ip_address_list:
	#check to see it the IP address passed is a valid host
	cmd = shlex.split("ping -n 1 ")
	cmd.append(each_ip)
	#print "cmd: ",cmd
	try:
		output = subprocess.check_output(cmd)
	except subprocess.CalledProcessError,e:
		print each_ip," is not valid"
		continue
	else:
		
		switch = Device(ip=each_ip,username='admin',password='cisco123')
		switch.open()
		shver_command_out = switch.show('show version')
		
		result = xmltodict.parse(shver_command_out[1])
		
		#print json.dumps(result, indent=4)
		
		sw_version = result['ins_api']['outputs']['output']['body']['kickstart_ver_str']
		sw_hostname = result['ins_api']['outputs']['output']['body']['host_name']
		sw_chassis = result['ins_api']['outputs']['output']['body']['chassis_id']
		sw_chassis_list = sw_chassis.split(' ')
		sw_model = sw_chassis_list[1]
		
		print "=" * 75
		print "\n\tHostname:",sw_hostname,"\n\tIP Address:",each_ip
		print "\tSwitch Model: ",sw_model
		
		if sw_version == app_version:
			print "\tNo upgrade required"
		else:
			print "\tUpgrade required from version: " + sw_version + " to version: " + app_version

print "=" * 75

current_time = time.ctime()
print "Created at: ",current_time