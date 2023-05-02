import sys
import os
from datetime import datetime
from netmiko import ConnectHandler

application_path = os.path.dirname(os.path.abspath(sys.argv[0]))


def run_script():
    username = 'puma'
    password = "cisco"

    bk_file_path = os.path.join(application_path, 'devices.txt')
    with open(bk_file_path) as f:
        devices_list = f.read().splitlines()

    enable_commands_file_path = os.path.join(application_path, 'enable_commands.txt')
    with open(enable_commands_file_path) as f:
        enable_commands = f.read().splitlines()

    for device in devices_list:
        print(f'Connecting to device "{device}"')
        ios_device = {
            'device_type': 'cisco_ios',
            'ip': device,
            'username': username,
            'password': password,
            'secret': password,
            'port': 22,
        }
        connection = ConnectHandler(**ios_device)
        print('Entering the enable mode...')

        connection.enable()

        for command in enable_commands:
            output = connection.send_command(command)
            print(output)

        output = connection.send_command('show run')
        prompt = connection.find_prompt()
        hostname = prompt[0:-1]

        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day

        output_directory = os.path.join(application_path, "BACKUP_SCH", "devices")
        os.makedirs(output_directory, exist_ok=True)
        filename = os.path.join(output_directory, f"{hostname}_{year}-{month}-{day}_update.txt")

        with open(filename, "w") as final:
            final.write(output)
            print(f"Backup of {hostname} completed successfully")
            print("#" * 30)

        print('Closing connection')
        connection.disconnect()


run_script()
