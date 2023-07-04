from netmiko import ConnectHandler
import shutil
from datetime import datetime
import os

# Path to the command file
command_file = 'command_file'

# Path to the devices file
devices_file = 'boxes.txt'

# Destination folder
backup_folder = 'BACKUP_SCH'

with open(command_file) as f:
    command_list = f.read().splitlines()

with open(devices_file) as f:
    devices_list = f.read().splitlines()

for device in devices_list:
    try:
        print("Connecting to device: " + device)
        ip_address_of_device = device
        ios_device = {
            'device_type': 'cisco_ios',
            'ip': ip_address_of_device,
            'username': 'xxxxx',
            'password': 'xxxxx'
        }

        net_connect = ConnectHandler(**ios_device)
        output = net_connect.send_config_from_file(command_file)
        print(output)

        prompt = net_connect.find_prompt()
        hostname = prompt[0:-1]

        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day

        filename = f'{hostname}_{year}-{month}-{day}_Backup01.txt'
        backup_file_path = os.path.join(backup_folder, filename)

        with open(backup_file_path, 'w') as final:
            final.write(output)
            print(f'Backup of {hostname} completed successfully')
            print('#' * 30)

        # Optional: Copy the backup file to the backup folder
        shutil.copy(backup_file_path, backup_folder)

    except Exception as e:
        print(f'Error occurred while backing up {device}: {str(e)}')
