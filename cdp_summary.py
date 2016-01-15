#!/usr/bin/python -tt
# cdp_summary
# Claudia
# PyCharm
__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "1/14/16  9:38 PM"
__copyright__ = "Copyright (c) 2015 Claudia"
__license__ = "Python"

# Import required modules
import sys
import re
import xmltodict
import json

from device import Device



def file_accessible(filepath, mode):
    ''' Check if a file exists and is accessible. Return True if it exists and return False otherwise '''
    try:
        f = open(filepath, mode)
        f.close()
    except IOError as e:
        return False

    return True

def get_hostname(sh_ver_cmd):

    result = xmltodict.parse(sh_ver_cmd[1])

    sw_hostname = result['ins_api']['outputs']['output']['body']['host_name']

    return sw_hostname


def qa_ipformat(ip2check):
    """
    This function takes in a string and checks to see if that string is formatted like an IP address.
    This is a "loose" match as it will accept 999.999.999.999.
    The function returs True if it is a valid IP and False otherwise.

    """

    ipresult = ''


    if re.match(r'^\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b$',ip2check):
        ipresult = True
    else:
        ipresult = False

    return (ipresult)


def main():
    """
    This is the main body of the script. This script reads in a file containing IP addresses and using the NX-OS API
    pulls CDP information from each device (IP) and stores it in a CSV file named cdp-output.csv in the local directory.

    """

    #Initialize the list data structure that will hold the IPs from the given file
    ip_list = []
    #Initialize the list data structure that will hold the cdp information extracted from each switch.
    #This will be a list of lists.
    nei_list = []

    #Store the path and filename provided as the first argument in the variable "ip_file_path"
    ip_file_path = sys.argv[1]

    #Using the file_accessible function, make sure that the file exists before trying to open it.
    ip_file_accessible = file_accessible(ip_file_path,'r')

    if ip_file_accessible:  # If the function file_accessible returned 'True' then the file is good and can be processed.
        ip_fh = open(ip_file_path, 'r')  # Open the file given as an argument which should contain one IP address per line
        ip_l = ip_fh.readlines() #Use the xxx.readlines() function to read in each line of the file into a list.
        # Using list comprehension populate the ip_list varialbe with valid IPs without leading or trailing CR,LF, or whitespace
        # within the list comprehension command call the qa_ipformat to ensure its a properly formatted IP string
        ip_list = [ip.strip() for ip in ip_l if len(ip)>0 and qa_ipformat(ip.strip())]
        #print "ip_list: ", ip_list  #Troubleshooting print statement. Should be commented out of working code.

    else:  # if the file_accessible function returned 'False' the file provided is not accessible and the script should end gracefully.
        #Function returned Fals so the file does not exist.  Print error and exit out of script.
        print("The file <" + ip_file_path + "> cannot be found. Please verify path and file name and try again.")
        sys.exit() #The file given in the command line is not accessible so print a notification and exit out of the script.

    # Define credentials to use for devices
    un = 'admin'
    pw = 'cisco123'

    #Header line printed to stdout (screen) to inform the user of what the script is doing.
    print "\n" + "="*20 + "Processing Devices in file " + ip_file_path + "="*20
    for dev_ip in ip_list:  #This for loop interates through each element of the list ip_list
        #print "\nProcessing device with IP: ",ip
        # Using the imported function Device in module device define the parameters to establish a session with the device.
        dev = Device(ip=dev_ip,username=un,password=pw)
        # Open a session to the device
        dev.open()
        # Run the 'show version' command to get the hostname of the device
        # First get the output of the command
        sh_ver_cmd_out = dev.show('show version')
        host_name = get_hostname(sh_ver_cmd_out)
        print "hostname from main(): ",host_name

        # Run the 'show cdp neighbor' command on the device and store the resulting output in cdp_cmd. This will return a tuple of dictionaries.
        cdp_cmd = dev.show('show cdp neighbor')
        # Take the command output stored in the second tuple [1] and store it in xlm format in the cdp_out variable
        # The cdp_out variable now has the actual 'show cdp neighbor' data
        cdp_out = xmltodict.parse(cdp_cmd[1])
        #print json.dumps(cdp_out, indent=3)  #Troubleshooting print statement. Should be commented out of working code.

        # Using the json.dumps output to determine the structure of the cdp_out dictionary or the "path" that must be walked to get to the values needed
        # The cdp_nei_list is a list of dictionaries. Each element describes the neighbor information.
        cdp_nei_list = cdp_out['ins_api']['outputs']['output']['body']['TABLE_cdp_neighbor_brief_info']['ROW_cdp_neighbor_brief_info']

        #print "cdp_nei_list: ", cdp_nei_list #Troubleshooting print statement. Should be commented out of working code.
        #print "lenght of cdp_nei_list: ",str(len(cdp_nei_list))  #Troubleshooting print statement. Should be commented out of working code.
        # Interate through each element of the list which contains a dictionary describint each cdp neighbor entry.
        for nei in cdp_nei_list:
            #print nei
            #Print the IP of the current switch, the id of the neighbor, the local interface, the platform of the neighbor and the neighbor or remote interface
            print dev_ip,nei['device_id'],host_name, nei['intf_id'],nei['platform_id'],nei['port_id']
            #record the values printed in a CSV format so each row describing a neighbor can be saved to a file at the end of processing
            nei_list.append(dev_ip + "," + host_name + "," + nei['device_id'] + "," + nei['intf_id'] + "," + nei['platform_id'] + "," + nei['port_id'] + "\n")

    #print nei_list #Troubleshooting print statement. Should be commented out of working code.
    #print len(nei_list) #Troubleshooting print statement. Should be commented out of working code.

    # Open a file that will be used to Write the neighbor results and name it 'cdp-output.csv'
    out_fh = open('cdp-output.csv','w')
    out_fh.write("Local IP, Local Hostname, Remote Hostname, Local Interface, Remote Model, Remote Interface \n")

    # Iterate through the nei_list list data structure and write a line to the output file for each element in the list representing a neighbor.
    for row in nei_list:
        # This command writes one "row" to the 'cdp-output.csv' file
        out_fh.write(row)

    # Close the cdp-output.csv file
    out_fh.close()



# Standard call to the main() function.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print '\nUsage:python cdp_summary <Full Path to file containing list of IP addresses to process>\nExample: python cdp_summary "/Users/Claudia/Dropbox (Indigo Wire Networks)/scripts/python/2016/aci_rotation"\n\nNote: File should contain one IP address per line.\n\n'
        sys.exit()
    else:
        main()
