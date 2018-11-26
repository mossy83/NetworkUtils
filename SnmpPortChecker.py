#!/bin/bash

from pysnmp.hlapi import *

def SnmpGet(SwitchIp, CommunityString, SnmpMib):
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in getCmd(SnmpEngine(),
    	                      CommunityData(CommunityString, mpModel=1),
                              UdpTransportTarget((SwitchIp, 161)),
                              ContextData(),
                              ObjectType(ObjectIdentity(SnmpMib["library"],SnmpMib["mib"],SnmpMib["position"])),
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
                #print(' = '.join([x.prettyPrint() for x in varBind]))
                return [x.prettyPrint() for x in varBind]

def main():
    SwitchIp = '172.30.186.153'
    CommunityString = 'MSAisNS859'
    #SnmpMib = '1.3.6.1.2.1.1.3.0' #System Uptime OID
    UptimeMib = {"library":"SNMP-FRAMEWORK-MIB","mib":"snmpEngineTime","position":0}
    daysUp = 1005
    uptime = SnmpGet(SwitchIp, CommunityString, UptimeMib)
    ParsedUptime = (int(uptime[1])/86400)
    #print ((int(uptime[1])/86400))
    if ParsedUptime < daysUp:
        print("The switch hasn't been up long enough\n")
        print("The switch has been up %d days" %ParsedUptime)
    else:
        print("Let's keep going")

if __name__ == '__main__':
    main()
