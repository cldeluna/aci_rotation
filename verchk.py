#!/usr/bin/python

import sys
from device import Device
import json
import xmltodict
import time


file_list = sys.argv
app_file_name = file_list[1]
ip_file_name = file_list[2]

file_object = open(app_file_name,"r")
app_version = file_object.readline().strip()
print "\nThis is the approved version: ",app_version,"\n\tSwitches not running this version will require an upgrade"

ip_file_object = open(ip_file_name,"r")
ip_addresses = ip_file_object.readline().strip()
ip_address_list = ip_addresses.split(',')

for each_ip in ip_address_list:
	
	switch = Device(ip=each_ip,username='admin',password='cisco123')
	switch.open()
	shver_command_out = switch.show('show version')

	result = xmltodict.parse(shver_command_out[1])

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