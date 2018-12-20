#!/bin/bash python3

import ipaddress, os, netmiko, platform, json
from getpass import getpass

def test_ip(ipadd):

    test_ip = ipaddress.ip_address(ipadd)
    print('Pinging: %s' %ipadd)

    if platform.system().lower() == 'windows':
        response = os.system('ping -n 1 ' + ipadd + ' > nul')
    else:
        response = os.system('ping -n 1 -c 1' + ipadd)

    if response == 0:
        return 0
    else:
        return 1

def ssh_connect(commands, **device):
        ssh = netmiko.ConnectHandler(**device)

        for command in commands:
            if 'show' in command:
                output = ssh.send_command(command)
                print('\n' + command)
                print('\n#####################################\n')
                print(output)
                print('\n#####################################\n')
            else:
                print('Using config mode')

def telnet_connect(**device):
    pass

def main():
    username = input('Enter your username: ')
    password = getpass('Enter your password: ')

    device_list = input('IP Address List - Json Formatted list: ' )
    command_list = input('Command list- Filename and extension: ')


    with open(device_list) as devices_json:
        devices = json.load(devices_json)

    with open(command_list) as cmd_list:
        commands = cmd_list.readlines()

    print(type(commands))
    for device in devices:
        device['username'] = username
        device['password'] = password

        print('Attempting to connect to %s' %device['ip'])
        print('######################################')
        try:
            ping_test = test_ip(device['ip'])
            if ping_test == 0:
                print('Creating an SSH connection to %s' %device['ip'])
                client = ssh_connect(commands, **device)
            else:
                print('%s didn\'t respond to ping. Skipping!!'%device['ip'])
        except Exception as e:
            print('There was an error connecting to %s' %device['ip'])
            print(e)

if __name__ == '__main__':
    main()
