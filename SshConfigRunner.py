#!/bin/bash python3

from netmiko import *
import getpass



def ssh_connect(commands, **device):
        ssh = ConnectHandler(**device)
        if len(commands) > 1:

            for command in commands:
                output = ssh.send_command(command)
                print(output)
                print('\n***************************************\n')
        else:
            output = ssh.send_command(commands[0])
            print(output)
            print('\n***************************************\n')

def telnet_connect(**device):
    pass

def main():

    print("hooray running scripts")

    device1 = {
    'device_type':'cisco_ios',
    'ip':'172.30.186.11',
    'username':'',
    'password': ''
    }

    device2 = {
    'device_type':'cisco_ios',
    'ip':'172.30.187.66',
    'username':'',
    'password': ''
    }

    devices = [device1, device2]
    commands = ['show interface status', 'show inventory']
    for device in devices:
        client = ssh_connect(commands, **device)

if __name__ == '__main__':
    main()
