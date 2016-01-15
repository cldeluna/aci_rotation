#!/usr/bin/python -tt
# cdp_summary
# Claudia
# PyCharm
__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "1/14/16  9:38 PM"
__copyright__ = "Copyright (c) 2015 Claudia"
__license__ = "Python"

import sys
import re
import xmltodict
import json

from device import Device



def file_accessible(filepath, mode):
    ''' Check if a file exists and is accessible. '''
    try:
        f = open(filepath, mode)
        f.close()
    except IOError as e:
        return False

    return True


def qa_ipformat(ip2check):
    """

    :param filename:
    :return:
    """

    ipresult = ''


    if re.match(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',ip2check):
        ipresult = True
    else:
        ipresult = False

    return (ipresult)


def main():

    ip_list = []
    nei_list = []

    #Store the path and filename provided as the first argument in the variable "ip_file_path"
    ip_file_path = sys.argv[1]

    #Using the file_accessible function, make sure that the file exists before trying to open it.
    ip_file_accessible = file_accessible(ip_file_path,'r')

    if ip_file_accessible:
        ip_fh = open(ip_file_path, 'r')
        ip_l = ip_fh.readlines()
        ip_list = [ip.strip() for ip in ip_l if len(ip)>0 and qa_ipformat(ip)]
        print "ip_list: ", ip_list

    else:
        #Function returned Fals so the file does not exist.  Print error and exit out of script.
        print("The file <" + ip_file_path + "> cannot be found. Please verify path and file name and try again.")
        sys.exit()

    # Define credentials to use for devices
    un = 'admin'
    pw = 'cisco123'

    print "\n" + "="*20 + "Processing Devices in file " + ip_file_path + "="*20
    for dev_ip in ip_list:
        print "\nProcessing device with IP: ",ip
        dev = Device(ip=dev_ip,username=un,password=pw)
        dev.open()
        cdp_cmd = dev.show('show cdp neighbor')
        #print cdp_cmd
        cdp_out = xmltodict.parse(cdp_cmd[1])
        print json.dumps(cdp_out, indent=3)

        cdp_nei_list = cdp_out['ins_api']['outputs']['output']['body']['TABLE_cdp_neighbor_brief_info']['ROW_cdp_neighbor_brief_info']

        print cdp_nei_list
        print str(len(cdp_nei_list))
        for nei in cdp_nei_list:
            #print nei
            print dev_ip,nei['device_id'],nei['intf_id'],nei['platform_id'],nei['port_id']
            nei_list.append(dev_ip + "," + nei['device_id'] + "," + nei['intf_id'] + "," + nei['platform_id'] + "," + nei['port_id'] + "\n")

    print nei_list
    print len(nei_list)

    out_fh = open('cdp-output.csv','w')

    for row in nei_list:
        out_fh.write(row)

    out_fh.close()



# Standard call to the main() function.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print '\nUsage:python cdp_summary <Full Path to file containing list of IP addresses to process>\nExample: python cdp_summary "/Users/Claudia/Dropbox (Indigo Wire Networks)/scripts/python/2016/aci_rotation"\n\nNote: File should contain one IP address per line.\n\n'
        sys.exit()
    else:
        main()
