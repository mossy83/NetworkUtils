#!/bin/bash python
from pysnmp.hlapi import *
import ipaddress

def ip_check(ip_add):
    try:
        check_ip = ipaddress.ip_address(ip_add)
        print ("Good")
    except ValueError:
        print(" is not a valid IP ")

class SNMPClient:

    def __init__(self, switch_ip, port, community):
        self.switch_ip = switch_ip
        self.port = port
        self.community = community

    def snmp_get(self, snmp_mib):
        snmp_get_data = []
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in getCmd(SnmpEngine(),
        	                      CommunityData(self.community, mpModel=1),
                                  UdpTransportTarget((self.switch_ip, self.port)),
                                  ContextData(),
                                  ObjectType(ObjectIdentity(snmp_mib["library"],snmp_mib["mib"],snmp_mib["position"])),
        						  lexicographicMode=False):

            if errorIndication:
                print(errorIndication)
                break
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                break
            else:
                for name, val in varBinds:
                    snmp_get_data.append(val)

                if len(snmp_get_data) == 1:
                    return snmp_get_data[0]
                else:
                    return snmp_get_data
                    #print(' = '.join([x.prettyPrint() for x in varBind]))
                    #return snmp_get_data

    def snmp_get_next(self, snmp_mib):
        results = []
        for (errorIndication,
            errorStatus,
            errorIndex,
            varBinds) in nextCmd(SnmpEngine(),
                          CommunityData( self.community,mpModel=1),
                          UdpTransportTarget(( self.switch_ip, self.port)),
                          ContextData(),
                          ObjectType(ObjectIdentity(snmp_mib["library"],snmp_mib["mib"])),
                          lexicographicMode=False):

            if errorIndication:
              print(errorIndication)
              break
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                break
            else:
                for varBind in varBinds:
                    results.append((" = ".join([x.prettyPrint() for x in varBind])))



        return results

                #return snmp_get_next_data



    def snmp_walk(self, snmp_mib):
        pass

def list_to_dict(input_list):
    for i in input_list:
        print(i)

def check_for_down_ints(switch_ints):
    results = []
    for x in switch_ints:
        if x[1] == 2:
            results.append(x)
    return results

def int_last_change(down_ints):
    split_dict = {}
    for x in down_ints:
        print (prettyPrint(x[0][1]))


def main():
    switch_ip = '172.30.186.11'
    community = 'MSAisNS859'
    days_up = 101


    checked_ip = ip_check(switch_ip)

    #Code block to verify that the switch has been up long enough
    uptime_mib = {"library":"SNMP-FRAMEWORK-MIB","mib":"snmpEngineTime","position":0}
    snmp_client = SNMPClient(switch_ip, 161, community)
    client_uptime = snmp_client.snmp_get(uptime_mib)

    #print (client_uptime)

    switch_days_up = client_uptime/86400
    if switch_days_up < days_up:
        print ("The switch hasn't been up long enough")
        print ("It has only been up %d days" %switch_days_up)
    #End block to verify sufficient switch uptime

    #Block to check port state
    port_state_mib = {"library":"IF-MIB", "mib":"ifOperStatus"}
    switch_int_status = snmp_client.snmp_get_next(port_state_mib)
    #print(switch_int_status)

    #End port state check
    #Convert the returned list to a dictionary
    interface_dict = list_to_dict(switch_int_status)

    '''
    #Block to find Availablity
    down_ints = check_for_down_ints(switch_int_status)
    #print(down_ints)
    last_change = int_last_change(down_ints)
    #print(last_change)
'''


if __name__ == '__main__':
    main()
