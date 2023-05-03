import sys
import os
import time
from datetime import datetime
from netmiko import ConnectHandler

application_path = os.path.dirname(os.path.abspath(sys.argv[0]))


def push_commands():
    username = 'puma'
    password = 'cisco'
    enable_password = 'cisco'

    devices_file_path = os.path.join(application_path, 'devices.txt')
    with open(devices_file_path) as f:
        devices_list = f.read().splitlines()

    config_commands = [
        'vlan 100',
        'name ADAPT1',
        'exit',
        'int vlan 100',
        'ip address 10.216.2.230 255.255.255.0',
        'exit',
        'username tron privilege 15 password cisco',
        'line con 0',
        'exec-timeout 30 30'
    ]

    for device in devices_list:
        print(f'Connecting to device "{device}"')
        ios_device = {
            'device_type': 'cisco_ios',
            'ip': device,
            'username': username,
            'password': password,
            'secret': enable_password,
            'port': 22,
            'timeout': 30,

        }

        connection = ConnectHandler(**ios_device)
        time.sleep(2) # Add a delay after connecting to the device
        print('Entering enable mode...')
        connection.enable()
        output = connection.send_config_set(config_commands)
        print(output)

        output = connection.send_command('show run')
        prompt = connection.find_prompt()
        hostname = prompt[0:-1]

        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day

        output_directory = os.path.join(application_path, 'BACKUP_SCH', 'devices')
        os.makedirs(output_directory, exist_ok=True)
        filename = os.path.join(output_directory, f'{hostname}_{year}-{month}-{day}_update.txt')

        with open(filename, 'w') as f:
            f.write(output)
            print(f"Backup of {hostname} completed successfully")
            print("#" * 30)

        print('Closing connection')
        connection.disconnect()


push_commands()
