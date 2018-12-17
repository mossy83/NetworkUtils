#!/bin/bash python3

import getpass, ipaddress, os, netmiko, platform


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

        if len(commands) > 1:
            print('Sending Multiple Commands')

            for command in commands:
                    output = ssh.send_command(command)
                    print('\n' + command)
                    print('\n#####################################\n')
                    print(output)
                    print('\n#####################################\n')

        else:
            output = ssh.send_command(commands[0])
            print(commands[0])
            print('\n#####################################\n')
            print(output)
            print('\n#####################################\n')

def telnet_connect(**device):
    pass

def main():
    username = input('Enter your username: ')
    password = getpass.getpass('Enter your password: ')

    ip_add_list = input('IP Address List - Filename and extension: ' )
    command_list = input('Command list- Filename and extension: ')
    '''
    device1 = {
    'device_type':'cisco_ios',
    'ip':'172.30.186.11',
    'username':username,
    'password': password
    }

    device2 = {
    'device_type':'cisco_ios',
    'ip':'172.30.187.66',
    'username': username,
    'password': password
    }

    devices = [device1, device2]
    commands = ['show inventory', 'show interface status']
    '''
    for device in devices:
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
