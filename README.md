# ACI Rotation Class January 2016

Dimension Data Team 2 ACI Rotation
Week 1 Project

Ideas:

- Find an IP (interface and mac) across a set of devices
- Find all Vlans across a set of devices
- Find serial numbers for a set of devices
- Find the IOS version for a set of devices and determine if an upgrade is needed
- Find the CDP neighbors for a set of devices.

Find the software version of a set of devices and determine if an upgrade is needed.

Inputs:  List of devices, Approved software version

- Provided as arguments on command line
- Provided in a text file Bonus

Pseudo code and logic:

For each device in a list of device IP addresses

- open each device
- run a “show version” command and save the output
- put the relevant output into a data structure that can be searched or “walked” (dict)
- extract the software version
- compare the extracted software version with an approved software version and print out if the version is OK or if it needs to be upgraded.  Provide a detailed statement.
    - Bonus: Add Model
    - Bonus: Add Hostname

Sample Output:

dhcp-171-71-130-176:aci_rotation Claudia$ python verchk.py "approved_version.txt" "ip_address.txt"

This is the approved version:  7.0(3)I2(3)
	Switches not running this version will require an upgrade
	
===========================================================================

	Hostname: N9k3
	IP Address: 172.31.217.135
	Switch Model:  C9396PX
	Upgrade required from version: 7.0(3)I1(1) to version: 7.0(3)I2(3)
===========================================================================

	Hostname: n9k6
	IP Address: 172.31.217.138
	Switch Model:  C9396PX
	Upgrade required from version: 7.0(3)I2(1) to version: 7.0(3)I2(3)
===========================================================================

	Hostname: 9k7
	IP Address: 172.31.217.142
	Switch Model:  C9396PX
	Upgrade required from version: 7.0(3)I2(1) to version: 7.0(3)I2(3)
===========================================================================

	Hostname: 9k8
	IP Address: 172.31.217.143
	Switch Model:  C9396PX
	Upgrade required from version: 7.0(3)I2(1) to version: 7.0(3)I2(3)
===========================================================================
Created at:  Thu Jan 14 14:43:39 2016
dhcp-171-71-130-176:aci_rotation Claudia$


Using the Dev-Net Sanbox switch:

dhcp-171-71-130-176:aci_rotation Claudia$ python verchk.py "approved_version.txt" "ip_address.txt"

This is the approved version:  7.0(3)I2(3)
	Switches not running this version will require an upgrade
	
===========================================================================

	Hostname: n9kvswitchfcs
	IP Address: 10.10.10.57
	Switch Model:  Chassis
	Upgrade required from version: 7.0(3)I2(1) to version: 7.0(3)I2(3)
===========================================================================
Created at:  Thu Jan 14 14:50:09 2016
dhcp-171-71-130-176:aci_rotation Claudia$
