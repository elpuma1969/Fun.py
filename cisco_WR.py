from netmiko import ConnectHandler
from getpass import getpass

# Read device IP addresses from the text file
with open("boxes.txt", "r") as file:
    device_ips = file.read().splitlines()

# Common authentication details
common_credentials = {
    "device_type": "cisco_ios",
    "username": "puma",
    "password": getpass(),
}

command = "copy running-config startup-config"

# Loop through the list of IP addresses
for ip in device_ips:
    device = {**common_credentials, "host": ip}

    net_connect = ConnectHandler(**device)
    output = net_connect.send_command_timing(
        command_string=command, strip_prompt=False, strip_command=False
    )
    
    if "Delete filename" in output:
        output += net_connect.send_command_timing(
            command_string="\n", strip_prompt=False, strip_command=False
        )
    if "?" in output:
        output += net_connect.send_command_timing(
            command_string="\n", strip_prompt=False, strip_command=False
        )

    net_connect.disconnect()

    print()
    print(f"Output from device {ip}:\n")
    print(output)
    print()
    print("-" * 80)
