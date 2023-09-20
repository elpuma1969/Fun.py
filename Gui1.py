import sys
import os
from datetime import datetime
from netmiko import ConnectHandler
import tkinter as tk
from tkinter import filedialog


def run_script(device_list, output_dir):
    username = 'XXXXX'
    password = "XXXXX"

    for device in device_list:
        ip_address_of_device = device
        ios_device = {
            'device_type': 'cisco_ios',
            'ip': ip_address_of_device,
            'username': username,
            'password': password,
            'secret': password,
            'port': 22,
        }

        try:
            connection = ConnectHandler(**ios_device)
            print(f'Connected to device: {device}')

            output = connection.send_command('show run')
            print(output)

            prompt = connection.find_prompt()
            hostname = prompt[0:-1]

            now = datetime.now()
            year = now.year
            month = now.month
            day = now.day

            filename = os.path.join(output_dir, f"{hostname}_{year}-{month}-{day}_DATA.txt")

            with open(filename, "w") as final:
                final.write(output)
                print(f"Backup of {hostname} completed successfully")
                print("#" * 30)

            connection.disconnect()
            print('Connection closed.')

        except Exception as e:

            print(f"Failed to connect to {device}: {str(e)}")


def browse_file():
    file_path = filedialog.askopenfilename(title="EVERYONE_CISCO_BACKUP.txt")
    device_list_entry.delete(0, tk.END)
    device_list_entry.insert(0, file_path)


def browse_output_dir():
    output_dir = filedialog.askdirectory(title="BACKUP_SCH")
    output_dir_entry.delete(0, tk.END)
    output_dir_entry.insert(0, output_dir)


def start_backup():
    device_list_file = device_list_entry.get()
    output_directory = output_dir_entry.get()

    if not device_list_file or not output_directory:
        status_label.config(text="Please select device list file and output directory.")
        return

    with open(device_list_file) as f:
        devices_list = f.read().splitlines()

    run_script(devices_list, output_directory)
    status_label.config(text="Backup completed.")


# Create the main window
root = tk.Tk()
root.title("Cisco Backup Tool")

# Create and arrange widgets
device_list_label = tk.Label(root, text="Device List File:", width='50', height='25')
device_list_label.pack()

device_list_entry = tk.Entry(root)
device_list_entry.pack()

browse_device_list_button = tk.Button(root, text="Browse", command=browse_file)
browse_device_list_button.pack()

output_dir_label = tk.Label(root, text="Output Directory:")
output_dir_label.pack()

output_dir_entry = tk.Entry(root)
output_dir_entry.pack()

browse_output_dir_button = tk.Button(root, text="Browse", command=browse_output_dir)
browse_output_dir_button.pack()

backup_button = tk.Button(root, text="Start Backup", command=start_backup)
backup_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
