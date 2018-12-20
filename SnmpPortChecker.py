#!/bin/bash python
from pysnmp.hlapi import *

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
    new_dict = {}
    for i in input_list:
        new_dict[(i.split('=')[0])] = (i.split('=')[1])
    return new_dict



def check_for_down_ints(switch_ints):
    results = []
    #For each entry, test if the interface is down
    #If down, append it to returned results
    for int, state in switch_ints.items():
        if state == ' down':
            results.append(int.split('.')[1])

    return results



def interface_last_change(snmp_client, days_down, down_ints):
    results = {}

    last_change_mib = {"library":"IF-MIB","mib":"ifLastChange","position":0}
    sys_uptime_mib = {"library":"SNMPv2-MIB","mib":"sysUpTime", "position":0}

    sys_uptime = snmp_client.snmp_get(sys_uptime_mib)

    for port in down_ints:
        last_change_mib["position"] = int(port)

        port_last_change = snmp_client.snmp_get(last_change_mib)

        port_down_time = (sys_uptime - port_last_change)/8640000

        if port_down_time > days_down:
            results[port] = port_down_time.prettyPrint()
    return results


def interface_name(snmp_client, port_list):
    results = {}
    interface_name_mib = {"library":"IF-MIB", "mib":"ifName", "position":0}

    for key, value in port_list.items():
        interface_name_mib["position"] = key

        port_name = snmp_client.snmp_get(interface_name_mib)

        if not port_name.prettyPrint().startswith("Vl"):
            results[port_name.prettyPrint()] = int(float(value))
    return results


def main():

    switch_ip = '172.30.186.11'
    community = 'MSAisNS859'
    days_down = 101


    #Code block to verify that the switch has been up long enough
    uptime_mib = {"library":"SNMP-FRAMEWORK-MIB","mib":"snmpEngineTime","position":0}
    snmp_client = SNMPClient(switch_ip, 161, community)
    client_uptime = snmp_client.snmp_get(uptime_mib)

    #print (client_uptime)

    switch_days_down = client_uptime/86400
    if switch_days_down < days_down:
        print ("The switch hasn't been up long enough")
        print ("It has only been up %d days" %switch_days_down)
    #End block to verify sufficient switch uptime

    #Block to check port state
    port_state_mib = {"library":"IF-MIB", "mib":"ifOperStatus"}
    switch_int_status = snmp_client.snmp_get_next(port_state_mib)
    #print(switch_int_status)

    #End port state check
    #Convert the returned list to a dictionary
    interface_dict = list_to_dict(switch_int_status)
    #print(interface_dict)
    #End conversion

    #Block to find Availablity
    down_ints = check_for_down_ints(interface_dict)
    #print(down_ints)

    last_change = interface_last_change(snmp_client, days_down, down_ints)
    #print(last_change)
    #End search for available ports

    available_ports = interface_name(snmp_client, last_change)
    #print(available_ports)
    #Output of available ports in a nice fashion
    print("Available Interfaces")
    print("Interface\tDays Down")
    for port, downtime in available_ports.items():
        print("%s\t\t%s" %(port, downtime))

    print("Total number of down ports: %s" %len(available_ports))

if __name__ == '__main__':
    main()
