import os
import sys
from datetime import datetime
from getpass import getpass

from netmiko import ConnectHandler

application_path = os.path.dirname(os.path.abspath(sys.argv[0]))

device_list = ["10.216.2.25", "10.216.124.2"]

password = getpass("Enter Password: ")

for device in device_list:
    try:
        print("Connecting to device " + device)
        ip_address_of_device = device
        cisco_1 = {
            'device_type': 'cisco_ios',
            'ip': ip_address_of_device,
            'username': "dsnyadmin",
            'password': password,

        }

        net_connect = ConnectHandler(**cisco_1)
        output = net_connect.send_command('show ip int brief')
        print(output)

        prompt = net_connect.find_prompt()
        hostname = prompt[0:-1]

        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day

        output_directory = os.path.join(application_path, 'backups', "bronx")
        os.makedirs(output_directory, exist_ok=True)
        filename = os.path.join(output_directory, f'{hostname}_{year}-{month}-{day}_update.txt')

        with open(filename, 'w') as f:
            f.write(output)
            print(f"Backup of {hostname} completed successfully")
            print("#" * 30)

        print('Closing connection')
        net_connect.disconnect()

    except Exception as e:
        print(f"Error occurred while backing up {device}: {str(e)}")








