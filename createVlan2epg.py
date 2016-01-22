#!/usr/bin/python -tt
# createTenant.py
# Claudia
# PyCharm
__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "1/19/16  1:10 PM"
__copyright__ = "Copyright (c) 2015 Claudia"
__license__ = "Python"

import sys
import lxml.etree as etree
import acitoolkit.acitoolkit as ACI
import urllib3
import requests
import re




def extract_vlans(vlan_file):
    vl_fh = open(vlan_file,'r')
    vlans = vl_fh.readlines()
    vlan_dict = {}
    row = 0
    for v in vlans:
        #print v
        vlan_row = v.split(',')
        #print "vlan_row", vlan_row
        if row > 1 and vlan_row[2] != "1":
            vlan_dict[vlan_row[2]]=vlan_row[3]
        row += 1
   #print "****Vlan Dictionary", vlan_dict

    return vlan_dict


def apic_login(hostname, username, password):
    url = "https://" + hostname
    sess = LoginSession(url, username, password)
    modir = MoDirectory(sess)
    try:
        modir.login()
    except:
        print "Login error!"
        exit(1)
    return modir
pass


def apic_login_acitk(hostname,username,password):

    # Login to APIC
    url = "https://" + hostname
    session = ACI.Session(url, username, password)
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to APIC')
        sys.exit(0)
    return session



def print_tenant(session):
    # Download all of the tenants
    #print "="*20 + "TENANT" + "="*20
    tenants = ACI.Tenant.get(session)
    tenant_list =[]
    #print "tenants", tenants
    for tenant in tenants:
        #print(tenant.name)
        tenant_list.append(tenant.name)
    return tenant_list


def main():

    epg_anp_dict = {}

    hostname, username, password, tenant_name, vlan_csv = sys.argv[1:]

    print "\n\n" + "="*20 + 'Creating Application Network Profiles and End Point Groups for each existing Vlan.' + "="*20
    print "="*10 + "Processing VLAN file " + vlan_csv +' for new Tenant ' + tenant_name + ' by user ' + username + " on APIC " + hostname + "="*10

    vlans = extract_vlans(vlan_csv)
    for vlan_id,vlan_name in vlans.items():
        #print vlan_id, vlan_name
        epg_name = "v"+vlan_id.strip()+"_"+vlan_name.upper().strip()+"_EPG"
        anp_name = "v"+vlan_id.strip()+"_"+vlan_name.upper().strip()+"_ANP"
        epg_anp_dict[anp_name]=epg_name
    #print epg_anp_dict

    print "="*10 + "Attempting to create Tenant " + tenant_name + ' by user ' + username + " on APIC " + hostname + "="*10

    print "\n\tLogging in to APIC"
    apic_session = apic_login_acitk(hostname, username, password)
    tenants = print_tenant(apic_session)
    #print "modir ",modir
    #print "tenant_name ", tenant_name
    if tenant_name in tenants:

        print "\n\t Tenant <"+tenant_name+ "> already exists and does not need to be created.\n"
        for t in tenants:
            print "\t Tenant "+t + " exists."
        print "\t\n Exiting Script.\n"
        sys.exit()

    else:

        print "\n\tCreating Tenant " + tenant_name + "\n"
        #create_tenant(modir, tenant_name)
        tenant = ACI.Tenant(tenant_name)

        #Configure a Private Network/VRF for the Tenant
        tenant_vrf = tenant_name + "_VRF"
        context = ACI.Context(tenant_vrf, tenant)


    for anp, epg in epg_anp_dict.items():

        # Create the App Profile, Bridge Domain, and EPG
        bd_name = re.sub("_EPG","_BD",epg )
        #print "bd_name: ",bd_name

        print "\tCreating Application Profile " + anp + " with EPG " + epg + " and BD " + bd_name
        aciapp = ACI.AppProfile(anp, tenant)
        aciepg = ACI.EPG(epg, aciapp)
        acibd = ACI.BridgeDomain(bd_name, tenant)

        #Add the BD to the context
        acibd.add_context(context)

        #Add the BD to the EPG
        aciepg.add_bd(acibd)

        # Push it all to the APIC
        resp = tenant.push_to_apic(apic_session)
        if not resp.ok:
            print('%% Error: Could not push configuration to APIC')
            print(resp.text)


    print "\nLogging out of APIC"
    #modir.logout()



# Standard call to the main() function.
if __name__ == '__main__':
    if len(sys.argv) != 6:
        print '\nUsage:python createVlan2epg.py <hostname> <username> <password> <tenant name> <anp name> <vlan csv file> \nExample: python createVlan2epg.py "172.18.180.187" "admin" "TSNaci123" "CdL520" "belfast-get-vlan.csv"\n\nNote: Fill in.\n\n'
        sys.exit()
    else:
        urllib3.disable_warnings()
        requests.packages.urllib3.disable_warnings()
        main()
