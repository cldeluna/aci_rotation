#!/usr/bin/python -tt
# getRouter
# Claudia
# PyCharm
__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "1/11/16  11:51 AM"
__copyright__ = "Copyright (c) 2015 Claudia"
__license__ = "Python"

import sys

def getRouter(rtr):
    router1 = {'os_version':'3.1.1','hostname':'nyc_router1','model':'nexus9396','domain':'cisco.com','mgmt_ip':'10.1.50.11'}
    router2 = dict( os_version='3.2.1', hostname='rtp_router2',model='nexus 9396',domain='cisco.com', mgmt_ip='10.1.50.12')
    router3 = dict( os_version='3.1.1', hostname='ROUTER3',model='nexus 9504',domain='lab.cisco.com', mgmt_ip='10.1.50.13')
    if rtr == 'router1':
        return router1
    elif rtr == 'router2':
        return router2
    elif rtr == 'router3':
        return router3
    return 'No router found.'




def main():
    data = getRouter(sys.argv[1])
    print("Data: ",data)



# Standard call to the main() function.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print '\nUsage:python getRouter <Argument 1>\nExample: python getRouter "/fill in"\n\nNote: Fill in.\n\n'
        sys.exit()
    else:
        main()
