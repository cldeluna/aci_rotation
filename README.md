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
