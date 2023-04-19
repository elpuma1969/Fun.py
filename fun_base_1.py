#!/usr/bin/env python
from getpass import getpass
from netmiko import ConnectHandler
from datetime import datetime


def read_file(file_name):
    with open(file_name) as f:
        content = f.read().splitlines()
    return content


def connect_to_device(device_ip, device_type, username, password, port=22):
    device = {
        'device_type': cisco_ios,
        'ip': device_ip,
        'username': username,
        'password': password,
        'port': port,
    }
    return ConnectHandler(**device)


def execute_commands(connection, commands):
    connection.enable()
    return connection.send_config_set(commands)


def save_output(output, hostname):
    now = datetime.now()
    filename = f'{hostname}_{now.year}-{now.month}-{now.day}_update.txt'
    with open(filename, 'w') as final:
        final.write(output)
        print(f'Backup of {hostname} completed successfully')
        print('#' * 30)


def main():
    username = input('Enter your SSH username: ')
    password = getpass()

    commands_list = read_file('command_file')
    devices_list = read_file('devices_file')

    for device_ip in devices_list:
        print('Connecting to device ' + device_ip)

        connection = connect_to_device(device_ip, 'cisco_ios', username, password)
        print('Entering the enable mode...')

        output = execute_commands(connection, commands_list)

        prompt = connection.find_prompt()
        hostname = prompt[0:-1]

        save_output(output, hostname)

        print('Closing connection')
        connection.disconnect()


if __name__ == '__main__':
    main()
