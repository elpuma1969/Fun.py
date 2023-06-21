#!/usr/bin/env python
from netmiko import ConnectHandler
from getpass import getpass

cisco1 = {
    "device_type": "cisco_ios",
    "host": "192.168.122.110",
    "username": "puma",
    "password": getpass()
}

create_vlan = input("Enter number of vlan: ")
name = input("Enter name of vlan: ")
intf = input("Enter Type of InterFace: ")
mode = input("Enter interface mode(access/trunk): ")
access_vlan = input("Enter number of vlan: ")

commands = [f"vlan {create_vlan}\n",
            f"name {name}\n",
            f"int fa{intf}\n",
            f"switchport mode {mode}\n",
            f"switchport access vlan {access_vlan}\n"]

with ConnectHandler(**cisco1) as net_connect:
    output3 = net_connect.send_config_set(commands)
print(output3)
