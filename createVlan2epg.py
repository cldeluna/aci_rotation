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
#from cobra.mit.session import LoginSession
#from cobra.mit.access import MoDirectory
#from cobra.mit.request import ConfigRequest
#from cobra.model.fv import Tenant
import lxml.etree as etree
import acitoolkit.acitoolkit as ACI


def extract_vlans(vlan_file):
    vl_fh = open(vlan_file,'r')
    vlans = vl_fh.readlines()
    vlan_dict = {}
    row = 0
    for v in vlans:
        print v
        vlan_row = v.split(',')
        print vlan_row
        if row > 1 and vlan_row[2] != "1":
            vlan_dict[vlan_row[2]]=vlan_row[3]
        row += 1
    print "****Vlan Dictionary", vlan_dict

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


def create_tenant(moDir, tenant_name):

    policy_universe = moDir.lookupByDn("uni")
    #
    fvTenantMo = Tenant(policy_universe, tenant_name)

    # print this querly in xml format
    #pol_uni = etree.parse(policy_universe)
    #print etree.tostring(pol_uni, pretty_print= True)
    #print toXMLStr(policy_universe prettyPrint=True)
    #print policy_universe

    # commit the change using a configrequest object
    configReq = ConfigRequest()
    configReq.addMo(fvTenantMo)
    moDir.commit(configReq)

pass



def print_tenant(session):
    # Download all of the tenants
    print "="*20 + "TENANT" + "="*20
    tenants = ACI.Tenant.get(session)
    tenant_list =[]
    print tenants
    for tenant in tenants:
        print(tenant.name)
        tenant_list.append(tenant.name)
    return tenant_list


def main():

    epg_anp_dict = {}

    hostname, username, password, tenant_name, vlan_csv = sys.argv[1:]


    vlans = extract_vlans(vlan_csv)
    for vlan_id,vlan_name in vlans.items():
        print vlan_id, vlan_name
        epg_name = "v"+vlan_id.strip()+"_"+vlan_name.upper().strip()+"_EPG"
        anp_name = "v"+vlan_id.strip()+"_"+vlan_name.upper().strip()+"_ANP"
        epg_anp_dict[anp_name]=epg_name
    print epg_anp_dict

    print "\nLogging in to APIC"
    apic_session = apic_login_acitk(hostname, username, password)
    tenants = print_tenant(apic_session)
    #print "modir ",modir
    #print "tenant_name ", tenant_name
    print "="*10 + "Attempting to create Tenant " + tenant_name + ' by user ' + username + " on APIC " + hostname + "="*10
    if tenant_name in tenants:

        print "\n\t Tenant <"+tenant_name+ "> already exists and does not need to be created."
    else:

        print "\n\tCreating Tenant " + tenant_name
        #create_tenant(modir, tenant_name)
        tenant = ACI.Tenant(tenant_name)

    for anp, epg in epg_anp_dict.items():

        # Create the Tenant, App Profile, and EPG
        #tenant = aci.Tenant(TENANT_NAME)
        aciapp = ACI.AppProfile(anp, tenant)
        aciepg = ACI.EPG(epg, aciapp)

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
        main()