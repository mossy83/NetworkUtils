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
                for varBind in varBinds:
                    print(' = '.join([x.prettyPrint() for x in varBind]))
                    return [x.prettyPrint() for x in varBind]

    def snmp_get_next(self, snmp_mib):
        pass
    def snmp_walk(self, snmp_mib):
        pass
def main():
    switch_ip = '172.30.186.153'
    community = 'MSAisNS859'
    days_up = 1011


    checked_ip = ip_check(switch_ip)
    #Code block to verify that the switch has been up long enough
    uptime_mib = {"library":"SNMP-FRAMEWORK-MIB","mib":"snmpEngineTime","position":0}
    snmp_client = SNMPClient(switch_ip, 161, community)
    client_uptime = snmp_client.snmp_get(uptime_mib)
    switch_days_up = int(client_uptime[1])/86400
    if switch_days_up < days_up:
        print ("The switch hasn't been up long enough")
        print ("It has only been up %d days" %switch_days_up)

if __name__ == '__main__':
    main()
