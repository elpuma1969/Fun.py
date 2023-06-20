from netmiko import ConnectHandler

def cp_run():
    with open('FULL_CISCO.txt') as f:
        devices_list = f.read().splitlines()

    for device in devices_list:
        print('Connecting to device: ' + device)
        ios_device = {
            'device_type': 'cisco_ios',
            'ip': device,
            'username': 'xxxxx',
            'password': 'xxxxx',
            'secret': 'xxxxx',
            'blocking_timeout': 20,
            'port': 22,
            'timeout': 120,
            'session_timeout': 120,
        }

        try:
            # Connect to the device
            connection = ConnectHandler(**ios_device)
            connection.enable()

            # Send the "copy running-config startup-config" command
            output = connection.send_command_timing('copy running-config startup-config',
                                                    strip_prompt=False, read_timeout=120)

            # Check the output for any error messages
            if 'Error:' in output or 'Failed to' in output:
                print(f'Error: {output}')

            # Check the output for the "Destination filename" prompt
            if 'Address or name of remote host' in output:
                # Send the "enter" key press to accept the default filename
                output += connection.send_command_timing('')

            # Check the output for the "Are you sure you want to save" prompt
            if 'Destination filename' in output:
                # Send "y" to confirm the save operation
                output += connection.send_command_timing("")

            # Disconnect from the device
            connection.disconnect()

            # Print the command output
            print(f'{device}: {output}')

        except Exception as e:
            print(f'Error connecting to device {device}: {str(e)}')

cp_run()
