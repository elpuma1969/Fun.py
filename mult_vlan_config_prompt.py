from netmiko import ConnectHandler
from getpass import getpass

# Read the device IP addresses from a text file
with open('boxes.txt', 'r') as file:
    device_ips = file.read().splitlines()

# Get the common device information from the user
username = input("Enter your username: ")
password = getpass("Enter your password: ")

# Prompt the user for VLAN and interface details
create_vlan = input("Enter number of VLAN: ")
name = input("Enter name of Name: ")
intf = input("Enter type of interface: ")
mode = input("Enter interface mode (access/trunk): ")
access_vlan = input("Enter number of access VLAN: ")

# Create a list to store the outputs for each device
outputs = []

# Iterate over each device IP address and configure VLAN settings
for ip in device_ips:
    device = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": username,
        "password": password
    }

    commands = [
        f"vlan {create_vlan}\n",
        f"name {name}\n",
        f"int fa{intf}\n",
        f"switchport mode {mode}\n",
        f"switchport access vlan {access_vlan}\n"
    ]

    with ConnectHandler(**device) as net_connect:
        output = net_connect.send_config_set(commands)

    outputs.append(output)

# Print the outputs for each device
for i, output in enumerate(outputs):
    print(f"\nOutput for Device {i + 1}:")
    print(output)
